#!/usr/bin/env python3
"""Validate the delivered stills without modifying any artwork."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets/concept_v3"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((ART / "manifest.json").read_text())
    provenance = json.loads((ART / "static_generation_manifest.json").read_text())
    sources = {a["file"]: a for a in provenance["assets"]}
    issues, rows, hashes = [], [], set()
    actions = manifest["actions"]
    if len(actions) != 14 or len({a["id"] for a in actions}) != 14:
        issues.append("Expected 14 unique actions.")
    if manifest.get("presentation") != "single_static_image":
        issues.append("Manifest does not declare single_static_image.")
    forbidden = {"frames", "fps", "duration", "duration_ms", "mp4", "webp", "timeline"}
    for action in actions:
        if forbidden.intersection(action):
            issues.append(f"Animation fields in {action['id']}")
        if set(action.get("images", {})) != {"male", "female"}:
            issues.append(f"Missing male/female pair: {action['id']}")
        for variant in ("male", "female"):
            file = action.get("images", {}).get(variant, "")
            expected = f"action_stills/{variant}/{action['id']}.png"
            if file != expected:
                issues.append(f"Unexpected path: {file}")
                continue
            path = ART / file
            if not path.is_file():
                issues.append(f"Missing {file}")
                continue
            digest = sha256(path)
            with Image.open(path) as im:
                width, height = im.size
                frame_count = getattr(im, "n_frames", 1)
                im.verify()
                if frame_count != 1:
                    issues.append(f"Image is not static: {file}")
                if width < 1200 or height < 675 or not 1.6 <= width / height <= 1.95:
                    issues.append(f"Unexpected native dimensions: {file} ({width}x{height})")
            if digest in hashes:
                issues.append(f"Duplicate artwork bytes: {file}")
            hashes.add(digest)
            source = sources.get(file)
            if not source or source.get("sha256") != digest or source.get("source_sha256") != digest:
                issues.append(f"Missing or mismatched original generation provenance: {file}")
            rows.append({"action": action["id"], "variant": variant, "file": file,
                         "width": width, "height": height, "frames": frame_count,
                         "bytes": path.stat().st_size, "sha256": digest})
    actual = {p.relative_to(ART).as_posix() for p in (ART / "action_stills").rglob("*.png")}
    if actual != {r["file"] for r in rows} or len(rows) != 28 or len(sources) != 28:
        issues.append("The manifest, provenance and delivered PNG set must each contain exactly 28 files.")
    report = {"version": "0.4", "status": "pass" if not issues else "fail",
              "presentation": "single_static_image", "actions": len(actions),
              "images": len(rows), "variants": {v: sum(r["variant"] == v for r in rows)
                                                for v in ("male", "female")},
              "native_generation_bytes_preserved": not issues,
              "visual_review": provenance.get("visual_review", {}),
              "issues": issues, "assets": rows}
    out = ART / "exports/static_asset_validation.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "actions", "images", "variants", "issues")},
                     ensure_ascii=False))
    raise SystemExit(bool(issues))


if __name__ == "__main__":
    main()
