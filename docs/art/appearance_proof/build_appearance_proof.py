#!/usr/bin/env python3
"""Build an offline SVG-layer UI proof from the saved appearance manifest.

This is a technical composition diagnostic, not production game artwork.
No generated concept image is edited or used as an appearance layer.
"""
from pathlib import Path
import json
import hashlib
import argparse

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT.parent / 'appearance_manifest.json')
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    profiles = manifest['profiles']
    assert len(profiles) == 48
    assert len({p['character_id'] for p in profiles}) == 48
    assert sum(p['group'] == 'active_staff' for p in profiles) == 45
    assert sum(p['group'] == 'recruit_candidates' for p in profiles) == 3
    assert len({(p['appearance']['face_shape'], p['appearance']['hair_family']) for p in profiles}) == 48
    assert len({(p['appearance']['body_type'], p['appearance']['hair_family']) for p in profiles}) == 48
    for key, minimum in [('body_type', 8), ('face_shape', 12), ('hair_family', 20), ('garment_structure', 10)]:
        assert len({p['appearance'][key] for p in profiles}) >= minimum, key
    template = (ROOT / 'proof_template.html').read_text(encoding='utf-8')
    data = json.dumps(manifest, ensure_ascii=False).replace('</', '<\\/')
    output = template.replace('__MANIFEST_DATA__', data)
    (ROOT / 'index.html').write_text(output, encoding='utf-8')
    print(json.dumps({'profiles': len(profiles), 'manifest_sha256': hashlib.sha256(args.manifest.read_bytes()).hexdigest(), 'html': str(ROOT / 'index.html')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
