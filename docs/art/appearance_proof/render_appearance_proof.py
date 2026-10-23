#!/usr/bin/env python3
"""Render and check the offline appearance composition proof with Chromium.

Requires playwright and Chromium. It does not run or test the Godot game.
"""
from pathlib import Path
import hashlib
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent


def main():
    page_errors = []
    manifest = ROOT.parent / 'appearance_manifest.json'
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_address[1]}/index.html'
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1)
        page.on('pageerror', lambda error: page_errors.append(str(error)))
        page.goto(url, wait_until='load')
        page.evaluate('document.fonts.ready')
        assert page.locator('#staff > .person').count() == 45
        assert page.locator('#recruits > .candidate').count() == 3
        assert page.locator('#staff svg').count() == 90
        assert page.locator('#recruits svg').count() == 6
        footer = page.locator('.foot').bounding_box()
        assert footer and footer['y'] + footer['height'] <= 1080, footer
        identities = page.evaluate('JSON.stringify(APPEARANCE_PROOF.profiles)')
        ids = page.evaluate('APPEARANCE_PROOF.profiles.map(p=>p.character_id)')
        assert len(set(ids)) == 48
        page.locator('[data-id="EMP-001"]').click()
        assert page.locator('#modal').evaluate("el=>el.classList.contains('open')")
        saved_profile = page.locator('#profile').inner_text()
        page.locator('[data-layer-key="hair_front"]').uncheck()
        hidden = page.locator('#bigArt [data-layer="hair_front"]').evaluate_all(
            "els=>els.every(el=>getComputedStyle(el).display==='none')")
        assert hidden
        assert page.locator('#profile').inner_text() == saved_profile
        page.locator('#close').click()
        page.reload(wait_until='load')
        page.evaluate('document.fonts.ready')
        assert identities == page.evaluate('JSON.stringify(APPEARANCE_PROOF.profiles)')
        page.screenshot(path=str(ROOT / '48_roster_proof.png'))
        roster_height = page.evaluate('document.querySelector(".foot").getBoundingClientRect().bottom')

        page.set_viewport_size({'width': 1600, 'height': 900})
        page.goto(url + '?view=layers', wait_until='load')
        page.evaluate('document.fonts.ready')
        assert page.locator('.layer-item').count() == 8
        assert page.locator('.proof-note').bounding_box()['y'] < 900
        page.screenshot(path=str(ROOT / 'portrait_layers_proof.png'))
        page.set_viewport_size({'width': 2400, 'height': 840})
        page.goto(url + '?view=wide', wait_until='load')
        page.evaluate('document.fonts.ready')
        assert page.locator('#staff > .person').count() == 48
        assert page.locator('#staff > .candidate-cell').count() == 3
        assert page.locator('.foot').bounding_box()['y'] + page.locator('.foot').bounding_box()['height'] <= 840
        page.screenshot(path=str(ROOT / '48_roster_wide.png'))
        assert not page_errors, page_errors
        browser.close()
    server.shutdown()

    data = json.loads(manifest.read_text(encoding='utf-8'))
    profiles = data['profiles']
    report = {
        'artifact_type': 'technical_svg_layer_composition_proof_not_final_game_art',
        'source_manifest': '../appearance_manifest.json',
        'source_manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
        'profiles': len(profiles),
        'staff': 45,
        'candidates': 3,
        'ids': ids,
        'coverage': {key: len({p['appearance'][key] for p in profiles}) for key in
                     ['body_type', 'face_shape', 'hair_family', 'garment_structure']},
        'unique_face_hair_pairs': len({(p['appearance']['face_shape'], p['appearance']['hair_family']) for p in profiles}),
        'unique_body_hair_pairs': len({(p['appearance']['body_type'], p['appearance']['hair_family']) for p in profiles}),
        'checks': {
            '45_staff_and_3_candidates_render': True,
            '96_svg_portrait_and_body_views_render': True,
            'staff_card_opens_saved_profile': True,
            'individual_layer_toggle_hides_same_layer_in_both_views': True,
            'layer_toggle_preserves_profile': True,
            'reload_preserves_all_48_profiles': True,
            'roster_footer_inside_1080px': True,
            'browser_script_errors': page_errors,
        },
        'screenshots': {'48_roster_proof.png': [1920, 1080], 'portrait_layers_proof.png': [1600, 900], '48_roster_wide.png': [2400, 840]},
        'roster_footer_bottom': roster_height,
    }
    (ROOT / 'proof_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
