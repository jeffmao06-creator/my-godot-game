#!/usr/bin/env python3
"""Package generated action grids as real frame sequences and silent animations.

Requires ImageMagick 7, FFmpeg, Pillow and NumPy. Pillow/NumPy are used only to
read pixels for validation. All extraction/encoding uses ImageMagick or FFmpeg.
Run after raw/sheets/*.png and action_definitions.json have been supplied.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True
from cut_grid import cut

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(command: list[str]) -> None:
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode:
        raise RuntimeError('Command failed: ' + repr(command) + '\n' + result.stderr[-5000:])


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def pixel_report(frames: list[Path], source: Path | None = None,
                 rects: list[dict] | None = None) -> dict:
    hashes, differences = [], []
    previous = None
    dimensions = set()
    source_pixels = None
    if source is not None:
        with Image.open(source) as image:
            source_pixels = np.asarray(image.convert('RGB'), dtype=np.uint8)
    for index, path in enumerate(frames):
        with Image.open(path) as image:
            dimensions.add(image.size)
            pixels = np.asarray(image.convert('RGB'), dtype=np.uint8)
        if source_pixels is not None:
            rect = rects[index]
            expected = source_pixels[rect['y']:rect['y'] + rect['height'],
                                     rect['x']:rect['x'] + rect['width']]
            if not np.array_equal(pixels, expected):
                raise ValueError(f'{path}: extracted RGB pixels differ from source rectangle')
        hashes.append(hashlib.sha256(pixels.tobytes()).hexdigest())
        if previous is not None:
            differences.append(round(float(np.abs(pixels.astype(np.int16) - previous).mean()) / 255, 6))
        previous = pixels.astype(np.int16)
    if len(dimensions) != 1:
        raise ValueError('Frame dimensions differ')
    if len(set(hashes)) != len(frames):
        raise ValueError('Duplicate pixel-identical frames in authored sheet')
    return {'dimensions': list(next(iter(dimensions))), 'unique_pixel_frames': len(set(hashes)),
            'pixel_sha256': hashes, 'adjacent_mean_absolute_rgb_difference': differences,
            'rgb_pixels_equal_source_rectangles': source_pixels is not None,
            'automated_check': 'nonduplicate frame content only; does not establish pose continuity',
            'manual_review': 'required: identity, poses, hands, prop positions and fixed-camera continuity'}


def encode_webp(frames: list[Path], durations: list[int], target: Path) -> None:
    command = ['magick']
    for path, duration in zip(frames, durations):
        command.extend(['-delay', f'{duration}/1000', str(path)])
    command.extend(['-loop', '0', '-quality', '92', '-define', 'webp:method=6', str(target)])
    execute(command)


def concat_escape(path: Path) -> str:
    return "'" + str(path.resolve()).replace("'", "'\\''") + "'"


def encode_mp4(frames: list[Path], durations: list[int], target: Path) -> None:
    with tempfile.TemporaryDirectory(prefix='law-action-encode-') as temp:
        listing = Path(temp) / 'frames.ffconcat'
        text = 'ffconcat version 1.0\n'
        for path, duration in zip(frames, durations):
            text += f'file {concat_escape(path)}\nduration {duration / 1000:.6f}\n'
        # concat demuxer requires a final image to make the previous duration visible.
        text += f'file {concat_escape(frames[-1])}\n'
        listing.write_text(text, encoding='utf-8')
        execute(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat',
                 '-safe', '0', '-i', str(listing), '-an', '-vf',
                 'pad=ceil(iw/2)*2:ceil(ih/2)*2,fps=25', '-c:v', 'libx264',
                 '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                 '-t', f'{sum(durations) / 1000:.6f}', '-movflags', '+faststart', str(target)])


def webp_report(path: Path, expected_frames: int, expected_ms: int) -> dict:
    with Image.open(path) as image:
        count = getattr(image, 'n_frames', 1)
        durations = []
        for index in range(count):
            image.seek(index)
            image.load()
            durations.append(int(image.info.get('duration', 0)))
    if count != expected_frames:
        raise ValueError(f'{path}: {count} encoded frames, expected {expected_frames}')
    if abs(sum(durations) - expected_ms) > 20:
        raise ValueError(f'{path}: {sum(durations)}ms, expected {expected_ms}ms')
    return {'encoded_frames': count, 'frame_durations_ms': durations, 'duration_ms': sum(durations)}


def video_report(path: Path, expected_ms: int) -> dict:
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    data = json.loads(result.stdout)
    streams = data.get('streams', [])
    video = [s for s in streams if s.get('codec_type') == 'video']
    if len(video) != 1 or any(s.get('codec_type') == 'audio' for s in streams):
        raise ValueError(f'{path}: expected one silent video stream')
    duration = round(float(data['format']['duration']) * 1000)
    if abs(duration - expected_ms) > 50:
        raise ValueError(f'{path}: {duration}ms video, expected {expected_ms}ms')
    return {'codec': video[0]['codec_name'], 'width': video[0]['width'],
            'height': video[0]['height'], 'duration_ms': duration, 'audio_streams': 0,
            'note': '25fps encoded playback holds 12 authored poses; repeated video frames are not extra drawn poses'}


def build_action(definition: dict, root: Path, with_video=True) -> tuple[dict, dict]:
    action_id = definition['id']
    if not action_id.replace('_', '').isalnum():
        raise ValueError(f'Unsafe action id {action_id}')
    source = root / definition.get('sheet', f'raw/sheets/{action_id}.png')
    layout = definition.get('sheet_layout', {})
    columns = int(layout.get('columns', definition.get('columns', 4)))
    rows = int(layout.get('rows', definition.get('rows', 3)))
    count = columns * rows
    folder = root / 'actions' / action_id
    frames = [folder / f'frame_{i:02}.png' for i in range(1, count + 1)]
    slice_report = cut(source, frames, columns, rows,
                       layout.get('margin', (0, 0, 0, 0)), layout.get('gutter', (0, 0)),
                       layout.get('cell_inset', (0, 0, 0, 0)))
    duration = int(definition.get('frame_duration_ms', 200))
    last_duration = int(definition.get('last_frame_duration_ms', 600))
    durations = list(definition.get('frame_durations_ms', [duration] * (count - 1) + [last_duration]))
    if len(durations) != count or min(durations) <= 0:
        raise ValueError(f'{action_id}: invalid duration list')
    report = pixel_report(frames, source, slice_report['rectangles'])
    animated = folder / 'preview.webp'
    poster = folder / 'poster.webp'
    execute(['magick', str(frames[0]), '-quality', '94', str(poster)])
    encode_webp(frames, durations, animated)
    report['animated_webp'] = webp_report(animated, count, sum(durations))
    video = folder / 'preview.mp4'
    if with_video:
        encode_mp4(frames, durations, video)
        report['mp4'] = video_report(video, sum(durations))
    action = copy.deepcopy(definition)
    action.update({'sheet': relative(source, root), 'frames': [relative(f, root) for f in frames],
                   'frame_durations_ms': durations, 'frame_count': count, 'fps': 1000 / duration,
                   'duration_ms': sum(durations), 'width': report['dimensions'][0],
                   'height': report['dimensions'][1], 'poster': relative(poster, root),
                   'animated_webp': relative(animated, root),
                   'animation_method': 'authored sequential poses; fixed-camera frame playback'})
    if with_video:
        action['mp4'] = relative(video, root)
    report.update({'id': action_id, 'sheet': relative(source, root), 'slice_map': slice_report,
                   'files': {relative(f, root): sha(f) for f in frames + [poster, animated] + ([video] if with_video else [])}})
    (folder / 'slice_map.json').write_text(json.dumps(slice_report, ensure_ascii=False, indent=2) + '\n')
    return action, report


def load_definitions(path: Path) -> tuple[dict, list[dict]]:
    value = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(value, list):
        return {}, value
    return {k: v for k, v in value.items() if k != 'actions'}, value['actions']


def verify(root: Path) -> dict:
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    report = json.loads((root / 'exports/asset_validation.json').read_text(encoding='utf-8'))
    expected = {a['id']: a for a in report['actions']}
    for action in manifest['actions']:
        saved = expected[action['id']]
        source = root / action['sheet']
        if sha(source) != saved['slice_map']['source_sha256']:
            raise ValueError(f'Source sheet changed since packaging: {action["id"]}')
        for name, digest in saved['files'].items():
            if sha(root / name) != digest:
                raise ValueError(f'File checksum mismatch: {name}')
        pixel_report([root / f for f in action['frames']], source,
                     saved['slice_map']['rectangles'])
        webp_report(root / action['animated_webp'], action['frame_count'], action['duration_ms'])
        if action.get('mp4'):
            video_report(root / action['mp4'], action['duration_ms'])
    summary = {'actions': len(manifest['actions']), 'png_frames': sum(a['frame_count'] for a in manifest['actions']),
               'all_frames_unique_within_each_action': True, 'animation_duration_ms': [a['duration_ms'] for a in manifest['actions']],
               'missing': manifest.get('missing_actions', []), 'checks': 'passed'}
    print(json.dumps(summary, ensure_ascii=False))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--definitions', type=Path)
    parser.add_argument('--allow-missing', action='store_true')
    parser.add_argument('--skip-video', action='store_true')
    parser.add_argument('--action', action='append', help='Package selected IDs only; requires --allow-missing for a partial manifest')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.check:
        verify(root)
        return
    for command in ['magick', 'ffmpeg']:
        if not shutil.which(command):
            raise SystemExit(f'Missing command: {command}')
    definitions_path = args.definitions or root / 'action_definitions.json'
    metadata, definitions = load_definitions(definitions_path)
    selected = set(args.action or [a['id'] for a in definitions])
    unknown = selected - {a['id'] for a in definitions}
    if unknown:
        raise SystemExit('Unknown action IDs: ' + ', '.join(sorted(unknown)))
    missing = [a['id'] for a in definitions if a['id'] not in selected
               or not (root / a.get('sheet', f"raw/sheets/{a['id']}.png")).is_file()]
    if missing and not args.allow_missing:
        raise SystemExit('Missing generated sheets: ' + ', '.join(missing))
    manifest_path = root / 'manifest.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    old_actions = {a['id']: a for a in manifest.get('actions', [])}
    manifest.update(metadata)
    actions, reports = [], []
    for definition in definitions:
        if definition['id'] in missing:
            continue
        action, report = build_action(definition, root, not args.skip_video)
        actions.append({**old_actions.get(action['id'], {}), **action})
        reports.append(report)
        print('Packaged ' + action['id'], flush=True)
    manifest.update({'actions': actions, 'missing_actions': missing,
                     'action_asset_status': 'complete_frame_exports' if not missing else 'partial_do_not_claim_complete',
                     'validation': 'exports/asset_validation.json'})
    (root / 'exports').mkdir(exist_ok=True)
    (root / 'exports/asset_validation.json').write_text(json.dumps(
        {'definitions': relative(definitions_path.resolve(), root), 'definitions_sha256': sha(definitions_path),
         'automatic_validation_scope': 'lossless cell extraction, unique pixels, file integrity, animation frame count and duration; artistic pose/identity continuity requires visual review',
         'actions': reports}, ensure_ascii=False, indent=2) + '\n')
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    verify(root)


if __name__ == '__main__':
    main()
