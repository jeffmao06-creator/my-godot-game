#!/usr/bin/env python3
"""Embed the real asset manifest for an offline, double-clickable preview."""
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=HERE.parent / 'manifest.json')
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8-sig'))
    if not manifest.get('actions'):
        raise SystemExit('No static action artwork in manifest; preview not generated.')
    output = HERE / 'manifest_data.js'
    source = '// Generated from ../manifest.json; do not edit by hand.\nwindow.CONCEPT_MANIFEST = '
    source += json.dumps(manifest, ensure_ascii=False, indent=2) + ';\n'
    catalog_path = HERE.parent / manifest.get('characters_path', 'character_catalog.json')
    if catalog_path.is_file():
        catalog = json.loads(catalog_path.read_text(encoding='utf-8-sig'))
        source += '\nwindow.CONCEPT_CHARACTERS = ' + json.dumps(catalog, ensure_ascii=False, indent=2) + ';\n'
    output.write_text(source, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
