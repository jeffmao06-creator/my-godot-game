#!/usr/bin/env python3
"""Merge exported PDFs, checksum all docs, and package the complete delivery.

Run after rebuilding the individual documents (see presentation/README.zh-TW.md).
Requires PyMuPDF. --check validates the existing PDFs, checksum list and ZIP.
"""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

import fitz

HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'Law_Firm_Simulator_Art_Package.zh-TW.zip'
SUMS = HERE / 'SHA256SUMS'
PDFS = {
    'presentation/Law_Firm_Simulator_Art_Pitch.zh-TW.pdf': 22,
    'art/Art_Production_Inventory.zh-TW.pdf': 16,
    'presentation/訴訟之神之路_贊助提案.pdf': 24,
}
COMPLETE = HERE / 'presentation/Law_Firm_Simulator_Complete_Proposal.zh-TW.pdf'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def files():
    return sorted(
        p for p in HERE.rglob('*')
        if p.is_file() and p != PACKAGE and p != SUMS
        and '__pycache__' not in p.parts and p.suffix != '.pyc'
    )


def check_pages():
    for name, expected in {**PDFS, str(COMPLETE.relative_to(HERE)): 38}.items():
        with fitz.open(HERE / name) as doc:
            if len(doc) != expected:
                raise ValueError(f'{name}: expected {expected} pages, got {len(doc)}')


def merge():
    pitch = HERE / next(iter(PDFS))
    inventory = HERE / 'art/Art_Production_Inventory.zh-TW.pdf'
    slides = json.loads((HERE / 'presentation/deck_content.json').read_text())['slides']
    with fitz.open() as out:
        with fitz.open(pitch) as source:
            out.insert_pdf(source)
        with fitz.open(inventory) as source:
            out.insert_pdf(source)
        toc = [[1, str(s.get('title', f'第 {i} 頁')).replace('\n', ' '), i]
               for i, s in enumerate(slides, 1)]
        toc.append([1, '完整美術設定與製作清單', 23])
        out.set_toc(toc)
        out.set_metadata({
            'title': '訴訟之神之路｜完整設計與美術提案 v0.2',
            'author': '訴訟之神之路',
            'subject': '22頁視覺簡報與16頁完整美術製作清單',
        })
        out.save(COMPLETE, garbage=4, deflate=True)


def build():
    merge()
    check_pages()
    entries = files()
    sums = ''.join(f'{digest(p.read_bytes())}  {p.relative_to(HERE).as_posix()}\n'
                   for p in entries)
    SUMS.write_text(sums, encoding='utf-8')
    with zipfile.ZipFile(PACKAGE, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for p in entries + [SUMS]:
            archive.write(p, 'docs/' + p.relative_to(HERE).as_posix())
    if PACKAGE.stat().st_size >= 100 * 1024 * 1024:
        raise ValueError('Package reaches GitHub 100 MiB file limit; split before publishing')


def check():
    check_pages()
    expected = {}
    for line in SUMS.read_text(encoding='utf-8').splitlines():
        sha, name = line.split('  ', 1)
        expected[name] = sha
        if digest((HERE / name).read_bytes()) != sha:
            raise ValueError(f'Checksum mismatch: {name}')
    actual_files = {p.relative_to(HERE).as_posix() for p in files()}
    if set(expected) != actual_files:
        raise ValueError('Checksum file does not match current individual document set')
    with zipfile.ZipFile(PACKAGE) as archive:
        if archive.testzip():
            raise ValueError('ZIP CRC validation failed')
        names = {'docs/' + name for name in expected} | {'docs/SHA256SUMS'}
        if set(archive.namelist()) != names:
            raise ValueError('ZIP file list differs from current document set')
        for name, sha in expected.items():
            if digest(archive.read('docs/' + name)) != sha:
                raise ValueError(f'Stale ZIP entry: {name}')
        if archive.read('docs/SHA256SUMS') != SUMS.read_bytes():
            raise ValueError('ZIP checksum list differs from current list')
    print(json.dumps({'individual_files': len(expected), 'pdf_pages': [22, 16, 38, 24],
                      'package_mib': round(PACKAGE.stat().st_size / 2**20, 2),
                      'zip_and_sha256': 'passed'}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not args.check:
        build()
    check()
