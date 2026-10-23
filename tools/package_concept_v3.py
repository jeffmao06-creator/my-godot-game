#!/usr/bin/env python3
"""Package the v0.3 illustrated assets and runnable previews; --check is read-only.

Historical v0.2 PDF/Word/ZIP files are not rebuilt or inserted into this package.
The current docs checksum list is refreshed without changing the historical ZIP.
"""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/concept_v3'
RELEASE = ROOT / 'releases'
ZIP = RELEASE / 'Illustrated_Art_Action_Cutscenes_v0.3.zip'
SUMS = RELEASE / 'Illustrated_Art_Action_Cutscenes_v0.3.SHA256SUMS'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def usable(path):
    return (path.is_file() and '__pycache__' not in path.parts
            and path.suffix not in ['.pyc', '.import', '.translation', '.zip']
            and '.godot' not in path.parts)


def artwork_files():
    # QA screenshots duplicate the delivered art at UI size. Keep them in Git;
    # package the reports and all original/usable artwork under the file limit.
    def included(path):
        rel = path.relative_to(ART)
        screenshot = (rel.parts[:2] == ('preview', 'qa')
                      and path.suffix.lower() in ['.png', '.jpg', '.webp'])
        return usable(path) and path.name != 'SHA256SUMS' and not screenshot
    return sorted(p for p in ART.rglob('*') if included(p))


def payload():
    extras = [
        ROOT / 'project.godot', ROOT / 'README.md',
        ROOT / '.gitignore', ROOT / '.gitattributes', Path(__file__).resolve(),
        ROOT / 'tools/.gdignore', ROOT / 'docs/GAME_DESIGN_PRD.zh-TW.md',
        ROOT / 'docs/art/ART_DIRECTION_v3.zh-TW.md', ROOT / 'docs/.gdignore',
    ]
    extras += [p for p in (ROOT / 'godot_demo').rglob('*') if usable(p)]
    return sorted(set(artwork_files() + [ART / 'SHA256SUMS'] + extras))


def check_assets():
    manifest = json.loads((ART / 'manifest.json').read_text())
    catalog = json.loads((ART / 'character_catalog.json').read_text())
    assert len(manifest['actions']) == 14 and not manifest.get('missing_actions')
    assert len(catalog['characters']) == 52
    for action in manifest['actions']:
        assert len(action['frames']) == 12
        assert sum(action['frame_durations_ms']) == 2800
        for name in action['frames'] + [action['poster'], action['animated_webp'], action['mp4']]:
            assert (ART / name).is_file(), name
    for character in catalog['characters']:
        assert sha((ART / character['file']).read_bytes()) == character['sha256']
    provenance = json.loads((ART / 'generation_manifest.json').read_text())
    for asset in provenance['assets']:
        assert sha((ART / asset['file']).read_bytes()) == asset['sha256']


def write_sums(base, paths, destination):
    lines = [f'{sha(p.read_bytes())}  {p.relative_to(base).as_posix()}\n' for p in paths]
    destination.write_text(''.join(lines), encoding='utf-8')


def build():
    check_assets()
    RELEASE.mkdir(exist_ok=True)
    write_sums(ART, artwork_files(), ART / 'SHA256SUMS')
    docs = ROOT / 'docs'
    doc_files = sorted(p for p in docs.rglob('*') if usable(p) and p.name != 'SHA256SUMS')
    write_sums(docs, doc_files, docs / 'SHA256SUMS')
    sources = payload()
    write_sums(ROOT, sources, SUMS)
    with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for source in sources:
            archive.write(source, source.relative_to(ROOT).as_posix())
        archive.write(SUMS, 'SHA256SUMS')
    if ZIP.stat().st_size >= 100 * 1024 * 1024:
        raise RuntimeError('Release exceeds GitHub 100 MiB per-file limit; split before pushing')


def check():
    check_assets()
    expected = {}
    for line in SUMS.read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        expected[name] = digest
        assert sha((ROOT / name).read_bytes()) == digest, name
    assert set(expected) == {p.relative_to(ROOT).as_posix() for p in payload()}
    with zipfile.ZipFile(ZIP) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(expected) | {'SHA256SUMS'}
        assert len(archive.namelist()) == len(expected) + 1
        for name, digest in expected.items():
            assert sha(archive.read(name)) == digest, f'Stale ZIP entry: {name}'
        assert archive.read('SHA256SUMS') == SUMS.read_bytes()
    print(json.dumps({
        'actions': 14, 'pose_frames': 168, 'character_pngs': 52,
        'environments': 2, 'files': len(expected),
        'zip_mib': round(ZIP.stat().st_size / 2**20, 2),
        'zip_sha256': sha(ZIP.read_bytes()), 'checksums_and_zip': 'passed',
    }, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not args.check:
        build()
    check()
