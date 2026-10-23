#!/usr/bin/env python3
"""Check actual static illustrations, manual dialogs and both protagonist versions."""
from pathlib import Path
import argparse
import functools
import hashlib
import http.server
import json
import threading
from playwright.sync_api import sync_playwright, Error

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=HERE / 'qa')
    args = parser.parse_args()
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((HERE.parent / 'manifest.json').read_text())
    catalog_path = HERE.parent / manifest.get('characters_path', 'character_catalog.json')
    catalog = json.loads(catalog_path.read_text())
    assert len(manifest['actions']) == 14, 'Expected 14 static action types.'
    assert len(catalog['characters'] if isinstance(catalog, dict) else catalog) == 52
    for action in manifest['actions']:
        assert set(action['images']) == {'male', 'female'}
        assert action['id'] != 'job_hop'
    expected_environments = len(manifest.get('environments', [])) or 2

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = 'http://127.0.0.1:' + str(server.server_port)
    url = origin + '/assets/concept_v3/preview/index.html'
    errors, requests, observations = [], [], []

    def ready(page):
        page.wait_for_function('window.actionArtworkPreview?.actions.length === 14 && window.assetGallery?.characters.length === 52')

    def artwork_ready(page):
        page.wait_for_function("document.querySelector('#artwork-dialog').open && document.querySelector('#artwork-loading').hidden && document.querySelector('#artwork-image').naturalWidth > 0")

    def all_images(page, selector):
        page.locator(selector).evaluate_all("(images) => images.forEach(image => image.loading = 'eager')")
        page.wait_for_function("(selector) => [...document.querySelectorAll(selector)].every(image => image.complete && image.naturalWidth > 0)", arg=selector)

    def image_contained(page):
        assert page.locator('#artwork-image').evaluate("""image => {
          const child = image.getBoundingClientRect(), parent = image.parentElement.getBoundingClientRect();
          return child.left >= parent.left - 1 && child.right <= parent.right + 1 &&
            child.top >= parent.top - 1 && child.bottom <= parent.bottom + 1;
        }"""), 'Image element must fit its visual container.'

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1600, 'height': 1100}, device_scale_factor=1)
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: requests.append(request.url))
            page.goto(url, wait_until='networkidle')
            ready(page)
            assert page.evaluate('window.CONCEPT_MANIFEST') == manifest
            assert page.evaluate('window.CONCEPT_CHARACTERS') == catalog
            assert page.locator('.action-card').count() == 14
            assert page.locator('video, audio, canvas').count() == 0
            assert page.evaluate('document.getAnimations().length') == 0
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert not page.locator('#artwork-dialog').evaluate('dialog => dialog.open')

            for gender in ('male', 'female'):
                page.locator('.hero [data-protagonist="' + gender + '"]').click()
                assert page.evaluate('window.actionArtworkPreview.variant') == gender
                all_images(page, '.action-card img')
                page.screenshot(path=str(out / ('library_' + gender + '.png')), full_page=True)
                actions = page.evaluate('window.actionArtworkPreview.actions.map(({id,title,images}) => ({id,title,images}))')
                for action in actions:
                    page.evaluate('id => window.actionArtworkPreview.open(id)', action['id'])
                    artwork_ready(page)
                    assert page.locator('#artwork-title').inner_text() == action['title']
                    image = page.locator('#artwork-image')
                    assert image.get_attribute('src') == action['images'][gender]
                    assert image.get_attribute('src').endswith('.png')
                    assert image.evaluate('image => image.naturalWidth >= 1000'), action['id'] + ' must be a full-size illustration.'
                    page.evaluate("""() => {
                      window.__imageChanges = 0;
                      window.__imageObserver = new MutationObserver(records => window.__imageChanges += records.length);
                      window.__imageObserver.observe(document.querySelector('#artwork-image'), {attributes:true, attributeFilter:['src']});
                    }""")
                    page.wait_for_timeout(1150)
                    assert page.locator('#artwork-dialog').evaluate('dialog => dialog.open')
                    assert image.get_attribute('src') == action['images'][gender]
                    assert page.evaluate('window.__imageChanges') == 0
                    assert page.evaluate('document.getAnimations().length') == 0
                    page.evaluate('window.__imageObserver.disconnect()')
                    observations.append({'id': action['id'], 'gender': gender, 'image': action['images'][gender].removeprefix(origin), 'held_unchanged_ms': 1150})
                    if action['id'] == 'write_brief':
                        page.screenshot(path=str(out / ('action_' + gender + '.png')))
                    page.locator('#continue-button').click()
                    assert not page.locator('#artwork-dialog').evaluate('dialog => dialog.open')
                page.wait_for_timeout(150)
                assert not page.locator('#artwork-dialog').evaluate('dialog => dialog.open')

            page.evaluate("window.actionArtworkPreview.setVariant('male')")
            page.locator('.action-card[data-id="consultation"]').click()
            artwork_ready(page)
            original_title = page.locator('#artwork-title').inner_text()
            male_src = page.locator('#artwork-image').get_attribute('src')
            page.locator('#dialog-variants [data-protagonist="female"]').click()
            artwork_ready(page)
            assert page.evaluate('window.actionArtworkPreview.currentActionId') == 'consultation'
            assert page.locator('#artwork-title').inner_text() == original_title
            assert page.locator('#artwork-image').get_attribute('src') != male_src
            assert '/female/' in page.locator('#artwork-image').get_attribute('src')
            assert page.locator('#dialog-variants [data-protagonist="female"]').evaluate('button => document.activeElement === button')
            page.keyboard.press('Escape')
            assert not page.locator('#artwork-dialog').evaluate('dialog => dialog.open')
            assert page.locator('.action-card[data-id="consultation"]').evaluate('button => document.activeElement === button')
            page.locator('#featured-view').click()
            artwork_ready(page)
            page.locator('#close-dialog').click()
            assert not page.locator('#artwork-dialog').evaluate('dialog => dialog.open')
            page.wait_for_timeout(150)
            assert not page.locator('#artwork-dialog').evaluate('dialog => dialog.open')
            assert page.locator('#featured-view').evaluate('button => document.activeElement === button')
            page.locator('#filters button').nth(1).focus()
            page.keyboard.press('Enter')
            assert page.locator('#filters button').nth(1).evaluate('button => document.activeElement === button')
            page.locator('#filters button').first.click()
            assert page.locator('.action-card').count() == 14

            page.locator('[data-view="characters"]').click()
            assert page.locator('.character-card').count() == 52
            all_images(page, '.character-card img')
            page.screenshot(path=str(out / 'characters.png'), full_page=True)
            for group, count in (('主角外觀', 4), ('事務所員工', 45), ('招募候選', 3)):
                page.locator('#character-filters button', has_text=group).click()
                assert page.locator('.character-card').count() == count
            candidate = page.locator('.character-card').first
            candidate.click()
            artwork_ready(page)
            assert page.locator('#dialog-variants').is_hidden()
            image_contained(page)
            page.screenshot(path=str(out / 'character_detail.png'))
            page.keyboard.press('Escape')
            assert candidate.evaluate('button => document.activeElement === button')

            page.locator('[data-view="environments"]').click()
            assert page.locator('.environment-card').count() == expected_environments
            all_images(page, '.environment-card img')
            page.screenshot(path=str(out / 'environments.png'), full_page=True)
            page.locator('.environment-card').first.click()
            artwork_ready(page)
            page.locator('#continue-button').click()

            mobile = browser.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
            mobile.on('pageerror', lambda error: errors.append(str(error)))
            mobile.on('request', lambda request: requests.append(request.url))
            mobile.goto(url + '?gender=female', wait_until='networkidle')
            ready(mobile)
            all_images(mobile, '.action-card img')
            assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert mobile.evaluate('window.actionArtworkPreview.variant') == 'female'
            mobile.screenshot(path=str(out / 'mobile.png'), full_page=True)
            mobile.locator('#featured-view').click()
            artwork_ready(mobile)
            assert '/female/' in mobile.locator('#artwork-image').get_attribute('src')
            assert mobile.locator('#continue-button').is_visible()
            image_contained(mobile)
            mobile.screenshot(path=str(out / 'mobile_action_female.png'))
            mobile.keyboard.press('Escape')
            assert mobile.locator('#featured-view').evaluate('button => document.activeElement === button')
            mobile.locator('[data-view="characters"]').click()
            mobile.locator('.character-card').first.click()
            artwork_ready(mobile)
            image_contained(mobile)
            mobile.screenshot(path=str(out / 'mobile_character.png'))

            offline = browser.new_page(viewport={'width': 1280, 'height': 900})
            offline.on('pageerror', lambda error: errors.append(str(error)))
            file_protocol_check = 'pass'
            try:
                offline.goto((HERE / 'index.html').as_uri() + '?gender=female', wait_until='load')
                ready(offline)
                offline.locator('#featured-view').click()
                artwork_ready(offline)
                assert offline.locator('#artwork-image').get_attribute('src').startswith('file:')
                offline.locator('#continue-button').click()
            except Error as error:
                if 'ERR_BLOCKED_BY_ADMINISTRATOR' not in str(error):
                    raise
                file_protocol_check = 'not_run: browser administrator policy blocks file:// navigation in this environment'
            browser.close()

        assert not errors, errors
        assert all(request.startswith(origin) for request in requests), 'Unexpected external dependency.'
        assert not any('preview.mp4' in request or 'preview.webp' in request or '/frame_' in request for request in requests)
        report = {
            'presentation': 'single_static_action_illustration',
            'action_count': 14, 'action_images': 28, 'character_count': 52, 'environment_count': expected_environments,
            'source_sha256': {
                'manifest': sha(HERE.parent / 'manifest.json'),
                'character_catalog': sha(catalog_path),
                'runtime': sha(HERE / 'runtime.js'),
                'style': sha(HERE / 'style.css'),
                'index': sha(HERE / 'index.html'),
                'embedded_data': sha(HERE / 'manifest_data.js'),
            },
            'checks': {
                'offline_embedded_manifest_and_catalog_match_source': True,
                'double_click_file_protocol_loads_female_action': file_protocol_check,
                'male_and_female_all_14_actions_load_full_size_png': True,
                'all_28_open_images_stay_unchanged_over_one_second': True,
                'manual_continue_close_and_escape': True,
                'no_automatic_close_or_reopen': True,
                'gender_switch_preserves_action_identity': True,
                'no_video_frame_sequence_or_css_animation': True,
                'no_legacy_animation_files_requested': True,
                'focus_returns_and_filters_keep_keyboard_focus': True,
                '52_characters_filter_4_45_3_and_fit_lightbox': True,
                'all_environments_load': True,
                'mobile_female_action_and_character_fit': True,
                'no_external_network_dependency': True,
                'browser_script_errors': [],
            },
            'observed_static_images': observations,
        }
        (out / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({key:value for key,value in report.items() if key != 'observed_static_images'}, ensure_ascii=False, indent=2))
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
