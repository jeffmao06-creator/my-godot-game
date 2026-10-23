#!/usr/bin/env python3
"""Extract complete transparent figures from generated character sheets.

Reads alpha components to locate full figures, retaining the source RGBA pixels.
ImageMagick separates neighboring figures and crops; it does not repaint or resize.
Requires scipy, numpy, Pillow and ImageMagick 7.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_sheet(root: Path, source: Path, ids: list[str], labels_text: list[str],
                  columns: int, kinds: list[str]) -> tuple[list[dict], dict]:
    with Image.open(source) as image:
        pixels = np.asarray(image.convert('RGBA'), dtype=np.uint8)
    alpha = pixels[:, :, 3]
    # A >4 component includes soft edges but avoids invisible A=1 bridges between figures.
    component_labels, _ = ndimage.label(alpha > 4)
    sizes = np.bincount(component_labels.ravel())
    sizes[0] = 0
    components = list(np.flatnonzero(sizes > 2000))
    if len(components) != len(ids):
        raise ValueError(f'{source.name}: {len(components)} full figures, expected {len(ids)}')
    boxes = ndimage.find_objects(component_labels)
    components.sort(key=lambda i: (boxes[i - 1][0].start + boxes[i - 1][0].stop) / 2)
    ordered = []
    for row in range(len(ids) // columns):
        group = components[row * columns:(row + 1) * columns]
        ordered.extend(sorted(group, key=lambda i: (boxes[i - 1][1].start + boxes[i - 1][1].stop) / 2))
    major_mask = np.isin(component_labels, ordered)
    distance, nearest = ndimage.distance_transform_edt(~major_mask, return_indices=True)
    owners = component_labels[nearest[0], nearest[1]]
    output_dir = root / 'characters/individual'
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    assigned = np.zeros(alpha.shape, dtype=bool)
    for index, (component, character_id, label, kind) in enumerate(zip(ordered, ids, labels_text, kinds)):
        # Only A<=4 fringe is assigned by proximity. Every A>4 source pixel of this
        # figure is preserved; pixels of neighboring figures are never included.
        keep = (owners == component) & (alpha > 0) & (distance <= 8)
        if np.any(assigned & keep):
            raise ValueError('Character extraction masks overlap')
        assigned |= keep
        ys, xs = np.nonzero(keep)
        if not len(xs):
            raise ValueError(f'Empty character {character_id}')
        x0, y0 = max(0, int(xs.min()) - 3), max(0, int(ys.min()) - 3)
        x1, y1 = min(alpha.shape[1], int(xs.max()) + 4), min(alpha.shape[0], int(ys.max()) + 4)
        mask = keep[y0:y1, x0:x1].astype(np.uint8) * 255
        output = output_dir / (character_id + '.png')
        with tempfile.TemporaryDirectory(prefix='law-char-mask-') as temporary:
            mask_file = Path(temporary) / 'extraction_mask.pgm'
            mask_file.write_bytes(f'P5\n{x1 - x0} {y1 - y0}\n255\n'.encode('ascii') + mask.tobytes())
            command = ['magick', str(source), '-crop', f'{x1-x0}x{y1-y0}+{x0}+{y0}', '+repage',
                       '(', str(mask_file), '-alpha', 'copy', ')', '-compose', 'DstIn',
                       '-composite', str(output)]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode:
                raise RuntimeError(result.stderr)
        with Image.open(output) as image:
            result_pixels = np.asarray(image.convert('RGBA'), dtype=np.uint8)
        original_roi = pixels[y0:y1, x0:x1]
        if not np.array_equal(result_pixels[mask > 0], original_roi[mask > 0]):
            raise ValueError(f'{character_id}: original figure RGBA changed during extraction')
        if np.any(result_pixels[:, :, 3][mask == 0]):
            raise ValueError(f'{character_id}: neighbor pixels were not removed')
        if np.any((component_labels == component) & ~keep):
            raise ValueError(f'{character_id}: foreground pixels omitted')
        records.append({'id': character_id, 'label': label, 'title': label, 'kind': kind,
                        'group': kind, 'source_sheet': source.relative_to(root).as_posix(),
                        'source_rect': {'x': x0, 'y': y0, 'width': x1-x0, 'height': y1-y0},
                        'source_component': int(component), 'file': output.relative_to(root).as_posix(),
                        'width': x1-x0, 'height': y1-y0, 'sha256': digest(output),
                        'source_figure_rgba_preserved': True,
                        'source_edge_touch': bool(xs.min() == 0 or ys.min() == 0 or xs.max() == alpha.shape[1]-1 or ys.max() == alpha.shape[0]-1)})
    return records, {'file': source.relative_to(root).as_posix(), 'sha256': digest(source),
                     'figures': len(records), 'alpha_threshold_for_components': 4,
                     'edge_fringe_radius_px': 8, 'all_source_figure_rgba_preserved': True,
                     'all_figure_alpha_pixels_preserved': True, 'neighbor_pixels_excluded': True,
                     'note': 'Only nearly transparent A<=4 pixels use nearest-component assignment; no RGB or shading is repainted.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    items, reports = [], []
    protagonists = ['PRO-M-WORK', 'PRO-M-HOME', 'PRO-F-WORK', 'PRO-F-HOME']
    names = ['男主角・工作服', '男主角・居家服', '女主角・工作服', '女主角・居家服']
    result, report = extract_sheet(root, root / 'characters/protagonist_variants_sheet.png',
                                   protagonists, names, 2, ['protagonist'] * 4)
    items.extend(result)
    reports.append(report)
    staff_ids = [f'EMP{i:03}' for i in range(1, 46)] + [f'REC{i:03}' for i in range(1, 4)]
    for index in range(4):
        ids = staff_ids[index*12:(index+1)*12]
        names = [('員工 ' if i.startswith('EMP') else '候選人 ') + i for i in ids]
        kinds = ['staff' if i.startswith('EMP') else 'candidate' for i in ids]
        result, report = extract_sheet(root, root / f'characters/staff_sheet_{index+1}.png', ids, names, 6, kinds)
        items.extend(result)
        reports.append(report)
    catalog = {'version': '0.3', 'game_name': '訴訟之神之路',
               'purpose': '概念插畫風透明立繪；不是可換裝的分層角色系統或動畫骨架',
               'counts': {'protagonist_variants': 4, 'staff': 45, 'candidates': 3, 'total_pngs': 52},
               'characters': items}
    (root / 'character_catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    (root / 'exports/character_validation.json').write_text(json.dumps(
        {'characters': len(items), 'sheets': reports, 'method': 'alpha-component separation and source-RGBA-preserving crop; no redrawing or resizing',
         'source_edge_touches': [i['id'] for i in items if i['source_edge_touch']],
         'manual_review': 'required: full body, shoes, hair, source drawing quality'}, ensure_ascii=False, indent=2) + '\n')
    manifest_path = root / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['characters_path'] = 'character_catalog.json'
    manifest['character_counts'] = catalog['counts']
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(catalog['counts'], ensure_ascii=False))


if __name__ == '__main__':
    main()
