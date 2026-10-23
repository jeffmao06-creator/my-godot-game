#!/usr/bin/env python3
"""Check the real-frame popup in Chromium and capture current artwork previews."""
from pathlib import Path
import argparse
import functools
import hashlib
import http.server
import json
import threading

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-actions', type=int, default=14)
    parser.add_argument('--expected-characters', type=int, default=52)
    parser.add_argument('--output-dir', type=Path, default=HERE / 'qa')
    args = parser.parse_args()
    manifest_path = HERE.parent / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    catalog_path = HERE.parent / manifest.get('characters_path', 'character_catalog.json')
    catalog = json.loads(catalog_path.read_text())
    assert len(manifest['actions']) == args.expected_actions
    assert len(catalog['characters']) == args.expected_characters
    args.output_dir.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f'http://127.0.0.1:{server.server_port}/assets/concept_v3/preview/'
    errors = []
    requests = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True)
            context = browser.new_context(viewport={'width': 1600, 'height': 1100})
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: requests.append(request.url))
            page.goto(url, wait_until='networkidle')
            page.wait_for_function('window.animationPreview && window.animationPreview.actions.length > 0')
            assert page.evaluate('window.CONCEPT_MANIFEST') == manifest, 'Offline manifest differs from source'
            assert page.locator('.action-card').count() == args.expected_actions
            assert 'job_hop' not in page.evaluate('window.animationPreview.actions.map(a => a.id)')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert page.locator('#stage-empty').is_hidden()
            assert page.locator('#featured-filmstrip img').count() == 12
            for image in page.locator('.action-card img').all():
                image.evaluate('(image) => image.loading = "eager"')
            page.wait_for_function('Array.from(document.querySelectorAll(".action-card img")).every(image => image.complete && image.naturalWidth > 0)')
            page.screenshot(path=str(args.output_dir / 'library.png'), animations='disabled')
            page.screenshot(path=str(args.output_dir / 'library_full.png'), full_page=True, animations="disabled")

            # Filters retain keyboard focus after updating the visible card set.
            category = page.locator('#filters button').nth(1)
            category.focus()
            category.press('Enter')
            assert category.evaluate('(button) => document.activeElement === button')
            page.locator('#filters button').first.click()

            actions = page.evaluate('window.animationPreview.actions.map(a => ({id:a.id,frames:a.frames.map(f=>f.url),duration:a.duration,durations:a.frames.map(f=>f.duration)}))')
            for action in actions:
                assert len(action['frames']) == 12
                assert action['durations'] == [200] * 11 + [600]
                assert action['duration'] == 2800
                page.evaluate('(id) => window.animationPreview.play(id)', action['id'])
                page.wait_for_function('document.querySelector("#transition-dialog").open && document.querySelector("#transition-loading").hidden')
                assert page.locator('#transition-image').get_attribute('src') in action['frames']
                page.locator('#skip-button').click()
                assert not page.locator('#transition-dialog').evaluate('(dialog) => dialog.open')

            # Check actual elapsed playback advances frames and auto-closes once.
            first = actions[0]
            page.evaluate('(id) => window.animationPreview.select(id)', first['id'])
            page.evaluate('''() => {
              const image = document.querySelector('#transition-image');
              window.__observedFrameSources = [];
              window.__frameObserver = new MutationObserver(() => window.__observedFrameSources.push(image.src));
              window.__frameObserver.observe(image, {attributes: true, attributeFilter: ['src']});
            }''')
            page.locator('#featured-play').click()
            page.wait_for_function('document.querySelector("#transition-loading").hidden')
            page.wait_for_timeout(230)
            page.evaluate('''() => {
              const until = performance.now() + 350;
              while (performance.now() < until) { /* Simulate a busy frame. */ }
            }''')
            page.wait_for_timeout(440)
            assert page.locator('#transition-image').get_attribute('src') != first['frames'][0]
            page.screenshot(path=str(args.output_dir / 'popup.png'), animations='disabled')
            page.wait_for_function('!document.querySelector("#transition-dialog").open', timeout=10000)
            observed = page.evaluate('window.__observedFrameSources')
            actual_pose_sequence = [source for source in observed if source in first['frames']]
            assert actual_pose_sequence == first['frames'], actual_pose_sequence
            page.evaluate('window.__frameObserver.disconnect()')
            assert page.locator('#featured-play').evaluate('(button) => document.activeElement === button')

            page.locator('#featured-play').click()
            page.wait_for_function('document.querySelector("#transition-loading").hidden')
            page.wait_for_timeout(350)
            page.evaluate('''() => {
              const image = document.querySelector('#transition-image');
              window.__replayFrameSources = [];
              window.__replayObserver = new MutationObserver(() => window.__replayFrameSources.push(image.src));
              window.__replayObserver.observe(image, {attributes: true, attributeFilter: ['src']});
            }''')
            page.locator('#replay-button').click()
            page.wait_for_function('document.querySelector("#transition-loading").hidden')
            page.wait_for_function('(first) => window.__replayFrameSources.includes(first)', arg=first['frames'][0])
            page.evaluate('window.__replayObserver.disconnect()')
            page.keyboard.press('Escape')
            assert not page.locator('#transition-dialog').evaluate('(dialog) => dialog.open')

            # A cancelled animation cannot close a later animation or retain timers.
            page.locator('#featured-play').click()
            page.locator('#skip-button').click()
            page.locator('#featured-play').click()
            page.wait_for_timeout(350)
            assert page.locator('#transition-dialog').evaluate('(dialog) => dialog.open')
            page.keyboard.press('Escape')

            page.emulate_media(reduced_motion='reduce')
            page.locator('#featured-play').click()
            page.wait_for_function('document.querySelector("#frame-status").textContent.includes("減少動態")')
            static_src = page.locator('#transition-image').get_attribute('src')
            page.wait_for_timeout(3100)
            assert page.locator('#transition-dialog').evaluate('(dialog) => dialog.open')
            assert page.locator('#transition-image').get_attribute('src') == static_src
            page.locator('#skip-button').click()
            page.emulate_media(reduced_motion='no-preference')

            # Real character PNGs and backgrounds are available from the same library.
            page.wait_for_function('(expected) => window.assetGallery && window.assetGallery.characters.length === expected', arg=args.expected_characters)
            assert page.evaluate('window.CONCEPT_CHARACTERS') == catalog
            page.locator('.resource-tab[data-view="characters"]').click()
            page.wait_for_timeout(650)
            assert page.locator('#character-panel').is_visible()
            assert page.locator('.character-card').count() == args.expected_characters
            for image in page.locator('.character-card img').all():
                image.evaluate('(image) => image.loading = "eager"')
            page.wait_for_function('Array.from(document.querySelectorAll(".character-card img")).every(image => image.complete && image.naturalWidth > 0)')
            page.screenshot(path=str(args.output_dir / 'characters.png'), animations='disabled')
            page.screenshot(path=str(args.output_dir / 'characters_full.png'), full_page=True, animations="disabled")
            for group, expected in [('主角外觀', 4), ('事務所員工', 45), ('招募候選', 3)]:
                page.locator('#character-filters button', has_text=group).click()
                assert page.locator('.character-card').count() == expected
            candidate = page.locator('.character-card').first
            candidate.click()
            assert page.locator('#transition-dialog').evaluate('(dialog) => dialog.open')
            assert page.locator('#replay-button').is_hidden()
            assert page.locator('#transition-progress-track').is_hidden()
            assert page.locator('#transition-image').evaluate('''image => {
              const picture = image.getBoundingClientRect();
              const frame = image.parentElement.getBoundingClientRect();
              return picture.top >= frame.top - 1 && picture.bottom <= frame.bottom + 1;
            }'''), 'Full character image exceeds the artwork viewport'
            page.screenshot(path=str(args.output_dir / 'character_detail.png'), animations='disabled')
            page.keyboard.press('Escape')
            assert candidate.evaluate('(button) => document.activeElement === button')
            page.locator('.resource-tab[data-view="environments"]').click()
            page.wait_for_timeout(650)
            assert page.locator('.environment-card').count() == 2
            page.wait_for_function('Array.from(document.querySelectorAll("#environment-grid img")).every(image => image.complete && image.naturalWidth > 0)')
            page.screenshot(path=str(args.output_dir / 'environments.png'), animations='disabled')
            page.locator('.environment-card').first.click()
            assert page.locator('#replay-button').is_hidden()
            assert page.locator('#transition-image').get_attribute('src').endswith('/environments/office.png')
            page.locator('#skip-button').click()
            page.locator('.resource-tab[data-view="actions"]').click()
            page.evaluate('(id) => window.animationPreview.play(id)', first['id'])
            page.wait_for_function('document.querySelector("#transition-loading").hidden')
            assert page.locator('#replay-button').is_visible()
            assert page.locator('#transition-progress-track').is_visible()
            page.locator('#skip-button').click()

            # Mobile keeps the original image visible and all controls in reach.
            mobile = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
            mobile_page = mobile.new_page()
            mobile_page.goto(url, wait_until='networkidle')
            mobile_page.wait_for_function('window.animationPreview')
            assert mobile_page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            mobile_page.screenshot(path=str(args.output_dir / 'mobile.png'), full_page=True, animations="disabled")
            mobile_page.locator('#featured-play').click()
            mobile_page.wait_for_function('document.querySelector("#transition-loading").hidden')
            assert mobile_page.locator('#skip-button').is_visible()
            mobile_page.locator('#skip-button').click()
            mobile_page.locator('.resource-tab[data-view="characters"]').click()
            mobile_page.wait_for_function('window.assetGallery && window.assetGallery.characters.length === 52')
            assert mobile_page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            mobile_page.locator('.character-card').first.click()
            assert mobile_page.locator('#skip-button').is_visible()
            assert mobile_page.locator('#transition-image').evaluate('''image => {
              const picture = image.getBoundingClientRect();
              const frame = image.parentElement.getBoundingClientRect();
              return picture.top >= frame.top - 1 && picture.bottom <= frame.bottom + 1;
            }'''), 'Mobile character image is cropped by the artwork viewport'
            mobile_page.screenshot(path=str(args.output_dir / 'mobile_character.png'), animations='disabled')
            mobile_page.locator('#skip-button').click()
            browser.close()
        assert not errors, errors
        assert all(request.startswith(url.split('/assets')[0]) for request in requests), 'External network dependency'
        report = {
            'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            'character_catalog_sha256': hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
            'runtime_sha256': hashlib.sha256((HERE / 'runtime.js').read_bytes()).hexdigest(),
            'action_count': args.expected_actions,
            'character_count': args.expected_characters,
            'environment_count': 2,
            'real_frames_per_action': 12,
            'duration_ms': 2800,
            'checks': {
                'offline_embedded_manifest_matches_source': True,
                'all_action_thumbnails_load': True,
                'all_actions_play_real_frames_and_skip': True,
                'frame_timing_11x200_plus_600_ms': True,
                'actual_frame_advancement': True,
                'busy_main_thread_preserves_all_twelve_poses': True,
                'auto_close_after_completion': True,
                'skip_escape_replay_and_reopen': True,
                'focus_return_and_filter_focus': True,
                'reduced_motion_static_preview': True,
                'mobile_no_horizontal_overflow': True,
                'all_52_character_pngs_load_and_filter_4_45_3': True,
                'character_lightbox_focus_and_static_controls': True,
                'full_character_image_fits_desktop_and_mobile_lightbox': True,
                'both_environment_images_load_and_open': True,
                'return_to_animation_restores_playback_controls': True,
                'no_external_network_dependency': True,
                'browser_script_errors': errors,
            },
        }
        (args.output_dir / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(report, ensure_ascii=False))
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
