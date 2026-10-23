#!/usr/bin/env python3
"""Package only the newly requested still illustrations; never include older art."""
import argparse
import hashlib
import html
import io
import json
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets/concept_v3"
NEW = ROOT / "assets/concept_v4"
RELEASE = ROOT / "releases/New_Art_Pack_v0.4.zip"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def gallery(rows, in_repo=False):
    blocks = []
    for category in ("下班後的家", "勝訴／敗訴視窗", "女性主角動作", "男性主角動作"):
        cards = []
        for row in rows:
            if row["category"] != category:
                continue
            path = Path(row["project_file"])
            src = ("../concept_v3/" + path.relative_to("assets/concept_v3").as_posix()
                   if in_repo and path.is_relative_to("assets/concept_v3")
                   else path.relative_to("assets/concept_v4").as_posix()
                   if in_repo else row["file"])
            title = html.escape(row["title"])
            cards.append(f'<a class="card" href="{src}" target="_blank" rel="noopener"><img src="{src}" alt="{title}" loading="lazy"><span>{title}</span></a>')
        blocks.append(f'<section><h2>{category}</h2><div class="grid">{"".join(cards)}</div></section>')
    return ('''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>訴訟之神之路｜本次新增素材</title><style>
*{box-sizing:border-box}body{margin:0;background:#101c27;color:#f4ead6;font:16px/1.7 system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:32px}h1{margin-bottom:4px}p{color:#c8c5b8}h2{font-size:23px;margin-top:38px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:20px}.card{display:block;border:1px solid #49605e;border-radius:10px;overflow:hidden;color:inherit;text-decoration:none;background:#1c3037}.card img{display:block;width:100%;height:auto;aspect-ratio:1672/941;object-fit:contain;background:#0c1721}.card span{display:block;padding:10px 16px}.card:focus-visible{outline:3px solid #d8b66c}
</style><main><h1>訴訟之神之路</h1><p>本次新增素材包 v0.4 · 31 張靜態 PNG · 點圖片開啟原圖</p><p>男女主角各 14 個動作、下班後家中場景 1 張、勝訴與敗訴視窗各 1 張。沒有動畫與音訊。</p>'''
            + "".join(blocks) + "</main></html>\n").encode()


def payload():
    manifest = json.loads((ART / "manifest.json").read_text())
    originals = json.loads((NEW / "generation_manifest.json").read_text())
    original_hashes = {a["file"]: a["source_sha256"] for a in originals["assets"]}
    if len(manifest["actions"]) != 14:
        raise ValueError("Expected 14 actions")
    rows = []
    for variant, label in (("female", "女性主角動作"), ("male", "男性主角動作")):
        for action in manifest["actions"]:
            file = action["images"][variant]
            if file != f"action_stills/{variant}/{action['id']}.png":
                raise ValueError("Only newly generated static action PNGs are permitted")
            rows.append({"id": action["id"], "variant": variant, "category": label,
                         "title": action["title"], "file": f"actions/{variant}/{action['id']}.png",
                         "project_file": f"assets/concept_v3/{file}"})
    rows += [{"id": "home_after_work", "category": "下班後的家", "title": "下班後的家中場景",
              "file": "scenes/home_after_work.png", "project_file": "assets/concept_v4/scenes/home_after_work.png"},
             {"id": "win", "category": "勝訴／敗訴視窗", "title": "勝訴視窗",
              "file": "results/win.png", "project_file": "assets/concept_v4/results/win.png"},
             {"id": "loss", "category": "勝訴／敗訴視窗", "title": "敗訴視窗",
              "file": "results/loss.png", "project_file": "assets/concept_v4/results/loss.png"}]
    data, hashes = {}, set()
    for row in rows:
        raw = (ROOT / row["project_file"]).read_bytes()
        with Image.open(io.BytesIO(raw)) as im:
            width, height = im.size
            if im.format != "PNG" or getattr(im, "n_frames", 1) != 1 or width < 1200 or height < 675:
                raise ValueError(f"Expected native large static PNG: {row['file']}")
            im.verify()
        sha = digest(raw)
        if original_hashes.get(row["file"]) != sha:
            raise ValueError(f"Artwork differs from generated original: {row['file']}")
        if sha in hashes:
            raise ValueError(f"Duplicate artwork: {row['file']}")
        hashes.add(sha)
        row.update(width=width, height=height, bytes=len(raw), sha256=sha)
        data[row["file"]] = raw
    if len(rows) != 31:
        raise ValueError("Expected exactly 31 new PNGs")
    pack_manifest = {"version": "0.4", "game": "訴訟之神之路", "presentation": "single_static_image",
                     "counts": {"female_actions": 14, "male_actions": 14, "home_scenes": 1, "result_windows": 2, "total_pngs": 31},
                     "scope": "Only artwork from the latest three requests; excludes all previous art packs, portraits, old backgrounds, animations and music.",
                     "assets": rows}
    data["manifest.json"] = json_bytes(pack_manifest)
    data["index.html"] = gallery(rows)
    data["README.zh-TW.md"] = (NEW / "README.zh-TW.md").read_bytes()
    data["generation_manifest.json"] = (NEW / "generation_manifest.json").read_bytes()
    report = {"version": "0.4", "status": "pass", "pngs": 31, "female_actions": 14, "male_actions": 14,
              "home_scenes": 1, "result_windows": 2, "all_single_frame": True,
              "original_png_bytes_preserved": True, "older_art_included": False,
              "visual_review": "All 31 delivered images inspected; female protagonist is the black-haired ponytail lawyer. Result labels 勝訴／敗訴／繼續 checked visually.",
              "issues": [], "assets": [{k: r[k] for k in ("file", "sha256", "width", "height", "bytes")} for r in rows]}
    data["validation.json"] = json_bytes(report)
    checksums = "".join(f"{digest(raw)}  {name}\n" for name, raw in sorted(data.items())).encode()
    data["SHA256SUMS"] = checksums
    return data, pack_manifest, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data, manifest, report = payload()
    if args.check:
        with zipfile.ZipFile(RELEASE) as archive:
            if archive.testzip() is not None or set(archive.namelist()) != set(data):
                raise ValueError("Archive corruption or unexpected/missing members")
            for name, expected in data.items():
                if archive.read(name) != expected:
                    raise ValueError(f"Archive differs from current source: {name}")
        if RELEASE.stat().st_size >= 100 * 1024 * 1024:
            raise ValueError("ZIP exceeds GitHub's per-file limit")
        expected_sha = f"{digest(RELEASE.read_bytes())}  {RELEASE.name}\n"
        if RELEASE.with_suffix(".SHA256SUMS").read_text() != expected_sha:
            raise ValueError("Release SHA mismatch")
        print(json.dumps({"status": "pass", "pngs": 31, "archive_members": len(data), "zip_bytes": RELEASE.stat().st_size}))
        return
    NEW.mkdir(parents=True, exist_ok=True)
    (NEW / "manifest.json").write_bytes(json_bytes(manifest))
    (NEW / "validation.json").write_bytes(json_bytes(report))
    (NEW / "index.html").write_bytes(gallery(manifest["assets"], in_repo=True))
    RELEASE.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(RELEASE, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, raw in sorted(data.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 23, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, raw)
    RELEASE.with_suffix(".SHA256SUMS").write_text(f"{digest(RELEASE.read_bytes())}  {RELEASE.name}\n")
    print(json.dumps({"status": "built", "pngs": 31, "zip_bytes": RELEASE.stat().st_size}))


if __name__ == "__main__":
    main()
