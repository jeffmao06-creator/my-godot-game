#!/usr/bin/env python3
"""Slice an authored grid with ImageMagick; never redraw or interpolate its art.

The grid boundaries are explicit. Uneven sheet dimensions use floor boundaries;
at most one trailing pixel per cell is omitted to keep frames equal in size.
Use --margin/--gutter only for borders that are visibly present in the source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def image_size(path: Path) -> tuple[int, int]:
    result = subprocess.run(
        ['magick', 'identify', '-format', '%w %h', str(path)],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return tuple(map(int, result.stdout.split()))


def rectangles(width: int, height: int, columns: int, rows: int,
               margin=(0, 0, 0, 0), gutter=(0, 0), inset=(0, 0, 0, 0)) -> list[dict]:
    left, top, right, bottom = map(int, margin)
    gx, gy = map(int, gutter)
    inset_left, inset_top, inset_right, inset_bottom = map(int, inset)
    usable_width = width - left - right - (columns - 1) * gx
    usable_height = height - top - bottom - (rows - 1) * gy
    if min(columns, rows, usable_width, usable_height) <= 0:
        raise ValueError('Invalid grid dimensions or margins')
    cell_width = usable_width // columns - inset_left - inset_right
    cell_height = usable_height // rows - inset_top - inset_bottom
    if min(cell_width, cell_height) <= 0:
        raise ValueError('Grid contains an empty cell')
    result = []
    for row in range(rows):
        for column in range(columns):
            x = left + column * gx + (column * usable_width) // columns + inset_left
            y = top + row * gy + (row * usable_height) // rows + inset_top
            result.append({'index': len(result) + 1, 'row': row, 'column': column,
                           'x': x, 'y': y, 'width': cell_width, 'height': cell_height})
    return result


def cut(source: Path, destinations: list[Path], columns: int, rows: int,
        margin=(0, 0, 0, 0), gutter=(0, 0), inset=(0, 0, 0, 0)) -> dict:
    if not shutil.which('magick'):
        raise RuntimeError('ImageMagick 7 (magick) is required')
    width, height = image_size(source)
    rects = rectangles(width, height, columns, rows, margin, gutter, inset)
    if len(destinations) != len(rects):
        raise ValueError(f'Expected {len(rects)} output paths, got {len(destinations)}')
    command = ['magick', str(source)]
    for target, rect in zip(destinations, rects):
        target.parent.mkdir(parents=True, exist_ok=True)
        geometry = f"{rect['width']}x{rect['height']}+{rect['x']}+{rect['y']}"
        command.extend(['(', '-clone', '0', '-crop', geometry, '+repage',
                        '-write', str(target), '+delete', ')'])
    command.append('null:')
    run(command)
    return {'source_width': width, 'source_height': height, 'columns': columns,
            'rows': rows, 'margin': list(margin), 'gutter': list(gutter),
            'cell_inset': list(inset),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'rectangles': rects,
            'processing': 'ImageMagick lossless region extraction; no redraw, resize or interpolation'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--columns', type=int, required=True)
    parser.add_argument('--rows', type=int, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--prefix', default='frame_')
    parser.add_argument('--margin', type=int, nargs=4, default=(0, 0, 0, 0),
                        metavar=('LEFT', 'TOP', 'RIGHT', 'BOTTOM'))
    parser.add_argument('--gutter', type=int, nargs=2, default=(0, 0), metavar=('X', 'Y'))
    parser.add_argument('--inset', type=int, nargs=4, default=(0, 0, 0, 0),
                        metavar=('LEFT', 'TOP', 'RIGHT', 'BOTTOM'))
    args = parser.parse_args()
    outputs = [args.output_dir / f'{args.prefix}{i:02}.png'
               for i in range(1, args.columns * args.rows + 1)]
    report = cut(args.source, outputs, args.columns, args.rows, args.margin, args.gutter, args.inset)
    report_path = args.output_dir / 'slice_map.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(report_path)


if __name__ == '__main__':
    main()
