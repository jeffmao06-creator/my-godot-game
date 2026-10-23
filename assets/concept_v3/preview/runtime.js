(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const rootURL = new URL('../', location.href);
  const params = new URLSearchParams(location.search);
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const categories = { daily: '工作日常', work: '工作日常', evening: '下班生活', leisure: '下班生活', event: '人與機會', events: '人與機會', management: '事務所經營' };
  const defaults = {
    breakfast: ['吃早餐', '讓忙碌的一天，先有一點熱氣。', '工作日常'],
    write_brief: ['寫書狀', '整理思緒，把每一段主張寫清楚。', '工作日常'],
    slack: ['摸魚', '和同事聊兩句，讓腦袋喘口氣。', '工作日常'],
    interview: ['面試新員工', '隔著一張桌子，認識未來的夥伴。', '事務所經營'],
    research: ['查找資料', '在書頁與判決之間，找到新的線索。', '工作日常'],
    flatter: ['拍老闆馬屁', '把話說得漂亮，也要看準時機。', '工作日常'],
    gym: ['健身', '把公事放下，專心完成下一組。', '下班生活'],
    standup: ['看脫口秀', '今晚，先把生活笑開一點。', '下班生活'],
    legal_video: ['看法律講座影片', '換一個地方，繼續理解這份工作。', '下班生活'],
    sleep: ['我只想睡覺', '關掉燈，讓今天到這裡就好。', '下班生活'],
    tv_program: ['上電視節目', '走進燈光，把法律說給更多人聽。', '人與機會'],
    news_interview: ['接受新聞採訪', '面對鏡頭，說出一段清楚的回答。', '人與機會'],
    consultation: ['客戶諮詢', '聽見故事，才能知道下一步怎麼走。', '人與機會'],
    assign_case: ['分派案件', '把文件交出去，也把信任交給夥伴。', '事務所經營'],
  };
  let actions = [];
  let featured = null;
  let filter = '全部';
  let current = null;
  let characterAssets = [];
  let characterFilter = '全部角色';
  let token = 0;
  let raf = null;
  let closingTimer = null;
  let returnFocus = null;
  const loaded = new Map();
  const dialog = $('transition-dialog');
  const asset = path => new URL(path, rootURL).href;
  const characterGroups = { protagonist: '主角外觀', player: '主角外觀', main: '主角外觀', staff: '事務所員工', employee: '事務所員工', candidate: '招募候選', recruit: '招募候選' };

  function normalize(raw, index) {
    const id = String(raw.id || raw.action_id || `action_${index + 1}`);
    const fallback = defaults[id] || [id, '', '動作過場'];
    const sourceFrames = Array.isArray(raw.frames) ? raw.frames : (raw.animation && raw.animation.frames) || [];
    const framePaths = sourceFrames.map(f => typeof f === 'string' ? f : f.src || f.path || f.file).filter(Boolean);
    const total = Number(raw.duration_ms || raw.animation?.duration_ms || 0);
    const fps = Number(raw.fps || raw.animation?.fps || 6);
    const frames = sourceFrames.map((f, i) => {
      const path = typeof f === 'string' ? f : f.src || f.path || f.file;
      const explicit = (typeof f === 'object' && Number(f.duration_ms || f.duration || 0)) || Number(raw.frame_durations_ms?.[i] || 0);
      const regular = Number(raw.frame_duration_ms || 0);
      const fallbackDuration = regular ? (i === framePaths.length - 1 ? Number(raw.last_frame_duration_ms || regular) : regular) : (total ? total / framePaths.length : 1000 / fps);
      return path ? { url: asset(path), duration: explicit || fallbackDuration } : null;
    }).filter(Boolean);
    const animationPath = typeof raw.animation === 'string' ? raw.animation : raw.animation?.src || raw.animation?.file || raw.animated_webp || raw.webp;
    const posterPath = raw.poster || raw.thumbnail || raw.preview;
    const categoryRaw = raw.category || fallback[2];
    const category = categories[categoryRaw] || categoryRaw;
    const duration = frames.length ? frames.reduce((sum, f) => sum + f.duration, 0) : total || 3000;
    if (!frames.length && !animationPath) return null;
    return {
      id, title: raw.title || raw.name || raw.label || fallback[0],
      description: raw.description || raw.caption || fallback[1], category,
      frames, duration, animationURL: animationPath ? asset(animationPath) : null,
      posterURL: posterPath ? asset(posterPath) : frames[0]?.url || asset(animationPath),
      index, aspectRatio: Number(raw.width) > 0 && Number(raw.height) > 0 ? `${Number(raw.width)} / ${Number(raw.height)}` : '16 / 9',
    };
  }

  function formatDuration(action) { return `${(action.duration / 1000).toFixed(1)} 秒`; }

  async function getManifest() {
    if (location.protocol === 'file:' && window.CONCEPT_MANIFEST) return window.CONCEPT_MANIFEST;
    try {
      const response = await fetch(new URL('manifest.json', rootURL), { cache: 'no-store' });
      if (!response.ok) throw new Error(`無法讀取素材清單（${response.status}）`);
      return await response.json();
    } catch (error) {
      if (window.CONCEPT_MANIFEST) return window.CONCEPT_MANIFEST;
      throw error;
    }
  }

  function imageElement(url, alt = '') {
    const image = document.createElement('img');
    image.src = url; image.alt = alt; image.decoding = 'async';
    return image;
  }

  function selectFeatured(action) {
    featured = action;
    $('featured-title').textContent = action.title;
    $('featured-description').textContent = action.description;
    $('featured-category').textContent = action.category;
    $('featured-stage').style.aspectRatio = action.aspectRatio;
    $('featured-meta').textContent = `${action.frames.length ? `${action.frames.length} 格` : '動畫'} · ${formatDuration(action)}`;
    const poster = $('featured-poster');
    poster.src = action.posterURL;
    poster.alt = `${action.title}的概念畫風過場畫面`;
    poster.hidden = false;
    $('stage-empty').hidden = true;
    $('featured-play').disabled = false;
    $('featured-filmstrip').replaceChildren(...action.frames.map((f, i) => imageElement(f.url, `第 ${i + 1} 格`)));
    document.querySelectorAll('.action-card').forEach(card => card.classList.toggle('is-featured', card.dataset.id === action.id));
  }

  function renderCards() {
    const visible = actions.filter(a => filter === '全部' || a.category === filter);
    $('library-count').textContent = `${visible.length} 段片刻${filter === '全部' ? '，自由選看' : ` · ${filter}`}`;
    $('action-grid').replaceChildren(...visible.map(action => {
      const card = document.createElement('button');
      card.type = 'button'; card.className = 'action-card'; card.dataset.id = action.id;
      card.setAttribute('aria-label', `播放${action.title}過場，${formatDuration(action)}`);
      const art = document.createElement('div'); art.className = 'card-art';
      const img = imageElement(action.posterURL); img.loading = 'lazy'; art.append(img);
      const play = document.createElement('span'); play.className = 'card-play'; play.setAttribute('aria-hidden', 'true'); art.append(play);
      const content = document.createElement('span'); content.className = 'card-content'; content.style.display = 'block';
      const line = document.createElement('span'); line.className = 'card-line';
      const title = document.createElement('span'); title.className = 'card-title'; title.textContent = action.title;
      const number = document.createElement('span'); number.className = 'card-index'; number.textContent = String(action.index + 1).padStart(2, '0');
      line.append(title, number);
      const description = document.createElement('span'); description.className = 'card-description'; description.textContent = action.description;
      const meta = document.createElement('span'); meta.className = 'card-meta';
      const category = document.createElement('span'); category.textContent = action.category;
      const time = document.createElement('span'); time.textContent = `${action.frames.length ? `${action.frames.length} 格 · ` : ''}${formatDuration(action)}`;
      meta.append(category, time); content.append(line, description, meta); card.append(art, content);
      card.addEventListener('click', () => { selectFeatured(action); openTransition(action, card); });
      card.classList.toggle('is-featured', featured?.id === action.id);
      return card;
    }));
  }

  function renderFilters() {
    const options = ['全部', ...new Set(actions.map(a => a.category))];
    $('filters').replaceChildren(...options.map(category => {
      const button = document.createElement('button'); button.type = 'button'; button.className = 'filter'; button.textContent = category;
      button.setAttribute('aria-pressed', String(filter === category));
      button.addEventListener('click', () => {
        filter = category;
        $('filters').querySelectorAll('button').forEach(option => option.setAttribute('aria-pressed', String(option === button)));
        renderCards();
      });
      return button;
    }));
  }

  function selectView(view, scroll = true) {
    const selected = ['actions', 'characters', 'environments'].includes(view) ? view : 'actions';
    document.querySelectorAll('.resource-tab').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === selected)));
    $('action-panel').hidden = selected !== 'actions';
    $('character-panel').hidden = selected !== 'characters';
    $('environment-panel').hidden = selected !== 'environments';
    if (scroll) $('material-navigation').scrollIntoView({ block: 'start', behavior: motion.matches ? 'auto' : 'smooth' });
  }

  document.querySelectorAll('.resource-tab').forEach(button => button.addEventListener('click', () => selectView(button.dataset.view)));

  function openArtwork(item, trigger) {
    token += 1; stopPlayback(); current = null; returnFocus = trigger || document.activeElement;
    $('transition-title').textContent = item.title;
    $('transition-category').textContent = item.category;
    $('transition-description').textContent = item.description || '';
    $('transition-image').src = item.url;
    $('transition-image').alt = item.title;
    $('transition-loading').hidden = true;
    $('transition-visual').setAttribute('aria-busy', 'false');
    $('transition-visual').classList.toggle('is-portrait', Boolean(item.portrait));
    $('transition-visual').style.aspectRatio = item.portrait ? '4 / 3' : '16 / 9';
    $('transition-progress-track').hidden = true;
    $('replay-button').hidden = true;
    $('frame-status').textContent = item.meta || '完整原圖';
    $('skip-button').textContent = '返回素材';
    $('close-dialog').setAttribute('aria-label', '關閉素材預覽');
    if (!dialog.open) dialog.showModal();
    document.body.style.overflow = 'hidden';
    $('skip-button').focus({ preventScroll: true });
  }

  function renderCharacterCards() {
    const visible = characterAssets.filter(character => characterFilter === '全部角色' || character.group === characterFilter);
    $('character-count').textContent = `${visible.length} 張完整立繪${characterFilter === '全部角色' ? '' : ` · ${characterFilter}`}`;
    $('character-grid').replaceChildren(...visible.map(character => {
      const card = document.createElement('button'); card.type = 'button'; card.className = 'character-card';
      card.dataset.id = character.id; card.setAttribute('aria-label', `檢視${character.title}完整立繪`);
      const art = document.createElement('span'); art.className = 'character-art';
      const image = imageElement(character.url); image.loading = 'lazy'; art.append(image);
      const caption = document.createElement('span'); caption.className = 'character-caption';
      const title = document.createElement('strong'); title.textContent = character.title;
      const label = document.createElement('small'); label.textContent = character.group;
      caption.append(title, label); card.append(art, caption);
      card.addEventListener('click', () => openArtwork({ ...character, category: character.group, portrait: true, description: '獨立透明人物立繪，保留完整身形與服裝細節。', meta: `透明 PNG${character.width && character.height ? ` · ${character.width} × ${character.height}` : ''}` }, card));
      return card;
    }));
  }

  function renderCharacterFilters() {
    const options = ['全部角色', ...new Set(characterAssets.map(character => character.group))];
    $('character-filters').replaceChildren(...options.map(group => {
      const button = document.createElement('button'); button.type = 'button'; button.className = 'filter'; button.textContent = group;
      button.setAttribute('aria-pressed', String(characterFilter === group));
      button.addEventListener('click', () => {
        characterFilter = group;
        $('character-filters').querySelectorAll('button').forEach(option => option.setAttribute('aria-pressed', String(option === button)));
        renderCharacterCards();
      });
      return button;
    }));
  }

  function renderCharacterSheets() {
    const sheets = [
      ['主角外觀', 'characters/protagonist_variants_sheet.png'],
      ...[1, 2, 3, 4].map(number => [`人物原稿 ${number}`, `characters/staff_sheet_${number}.png`]),
    ];
    sheets.forEach(([title, path]) => {
      const link = document.createElement('a'); link.href = asset(path); link.target = '_blank'; link.rel = 'noopener'; link.textContent = title;
      $('sheet-links').append(link);
    });
    return sheets;
  }

  async function loadCharacters(manifest) {
    const catalogPath = typeof manifest.characters_path === 'string' ? manifest.characters_path : 'character_catalog.json';
    let catalog = window.CONCEPT_CHARACTERS;
    if (location.protocol !== 'file:' || !catalog) {
      try {
        const response = await fetch(new URL(catalogPath, rootURL), { cache: 'no-store' });
        if (response.ok) catalog = await response.json();
      } catch (_) { /* The embedded catalog is the offline fallback. */ }
    }
    let list = Array.isArray(catalog) ? catalog : catalog?.characters || catalog?.assets || [];
    if (!Array.isArray(list)) list = Object.entries(list).map(([id, entry]) => ({ id, ...entry }));
    if (!list.length && catalog) {
      list = ['protagonists', 'staff', 'candidates'].flatMap(group => (catalog[group] || []).map(item => ({ group: group === 'protagonists' ? 'protagonist' : group === 'candidates' ? 'candidate' : 'staff', ...item })));
    }
    characterAssets = list.map((item, index) => {
      const id = item.id || item.character_id || `character_${index + 1}`;
      const path = item.file || item.png || item.path || item.src || item.image;
      const groupRaw = item.group || item.role || item.type || (String(id).startsWith('EMP') ? 'staff' : String(id).startsWith('REC') ? 'candidate' : 'protagonist');
      return path ? { id, title: item.title || item.name || item.display_name || id, url: asset(path), group: characterGroups[groupRaw] || groupRaw, width: item.width, height: item.height } : null;
    }).filter(Boolean);
    if (characterAssets.length) {
      $('character-tab-count').textContent = characterAssets.length;
      renderCharacterFilters(); renderCharacterCards();
    } else {
      const sheets = renderCharacterSheetsFallback();
      $('character-count').textContent = `${sheets.length} 張人物原稿`;
      $('character-tab-count').textContent = sheets.length;
    }
    window.assetGallery = { get characters() { return characterAssets; }, selectView };
  }

  function renderCharacterSheetsFallback() {
    const sheets = [
      { title: '主角外觀原稿', path: 'characters/protagonist_variants_sheet.png' },
      ...[1, 2, 3, 4].map(number => ({ title: `人物原稿 ${number}`, path: `characters/staff_sheet_${number}.png` })),
    ];
    $('character-grid').replaceChildren(...sheets.map(sheet => {
      const card = document.createElement('button'); card.type = 'button'; card.className = 'environment-card';
      const art = document.createElement('span'); art.className = 'environment-art'; art.append(imageElement(asset(sheet.path), sheet.title));
      const caption = document.createElement('span'); caption.className = 'environment-caption'; caption.textContent = sheet.title;
      card.append(art, caption);
      card.addEventListener('click', () => openArtwork({ title: sheet.title, category: '人物原稿', url: asset(sheet.path), description: '完整原稿，供人物外觀與服裝參照。' }, card));
      return card;
    }));
    return sheets;
  }

  function renderEnvironments() {
    const environments = [
      { title: '雨天辦公室', description: '雨窗、文件和暖燈，陪你度過忙碌的一天。', path: 'environments/office.png' },
      { title: '下班後的家', description: '把公事放在門邊，留一盞燈給自己。', path: 'environments/home.png' },
    ];
    $('environment-tab-count').textContent = environments.length;
    $('environment-count').textContent = `${environments.length} 個完整空間`;
    $('environment-grid').replaceChildren(...environments.map(environment => {
      const card = document.createElement('button'); card.type = 'button'; card.className = 'environment-card';
      card.setAttribute('aria-label', `檢視${environment.title}完整場景`);
      const art = document.createElement('span'); art.className = 'environment-art';
      const image = imageElement(asset(environment.path)); image.loading = 'lazy'; art.append(image);
      const caption = document.createElement('span'); caption.className = 'environment-caption';
      const title = document.createElement('strong'); title.textContent = environment.title;
      const description = document.createElement('small'); description.textContent = environment.description;
      caption.append(title, description); card.append(art, caption);
      card.addEventListener('click', () => openArtwork({ title: environment.title, description: environment.description, category: '生活場景', url: asset(environment.path), meta: '完整場景原圖' }, card));
      return card;
    }));
  }

  function preload(url) {
    if (loaded.has(url)) return loaded.get(url);
    const promise = new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image); image.onerror = () => reject(new Error('圖片無法載入'));
      image.src = url;
    });
    loaded.set(url, promise);
    promise.catch(() => loaded.delete(url));
    return promise;
  }

  function stopPlayback() {
    if (raf !== null) cancelAnimationFrame(raf);
    if (closingTimer !== null) clearTimeout(closingTimer);
    raf = closingTimer = null;
  }

  function closeTransition() {
    token += 1; stopPlayback();
    if (dialog.open) dialog.close();
    current = null;
    document.body.style.overflow = '';
    if (returnFocus && returnFocus.isConnected) returnFocus.focus({ preventScroll: true });
  }

  async function play(action) {
    const mine = ++token; stopPlayback();
    $('transition-image').src = action.posterURL;
    $('transition-image').alt = `${action.title}過場`;
    $('transition-progress').style.transform = 'scaleX(0)';
    $('transition-loading').hidden = false;
    $('transition-visual').setAttribute('aria-busy', 'true');
    $('frame-status').textContent = '準備畫面中';
    $('skip-button').textContent = '略過';
    try {
      await Promise.all((action.frames.length ? action.frames.map(f => f.url) : [action.animationURL]).map(preload));
    } catch (error) {
      if (mine !== token) return;
      $('transition-loading').hidden = true;
      $('transition-visual').setAttribute('aria-busy', 'false');
      $('frame-status').textContent = '素材未能完整載入，請確認下載包包含所有影格。';
      $('skip-button').textContent = '返回素材';
      return;
    }
    if (mine !== token || !dialog.open) return;
    $('transition-loading').hidden = true;
    $('transition-visual').setAttribute('aria-busy', 'false');
    if (motion.matches) {
      $('transition-image').src = action.posterURL;
      $('frame-status').textContent = '已依系統偏好減少動態，顯示靜態畫面。';
      $('skip-button').textContent = '返回素材';
      return;
    }
    $('transition-image').src = action.frames.length ? action.frames[0].url : action.animationURL;
    let started = null;
    let frameStarted = null;
    let completedDuration = 0;
    let index = 0;
    function tick(now) {
      if (mine !== token || !dialog.open) return;
      if (started === null) started = now;
      if (frameStarted === null) frameStarted = now;
      let elapsed;
      let finished;
      if (action.frames.length) {
        // Preserve every actual pose under load. A slow renderer extends the
        // scene rather than jumping over intermediate frame illustrations.
        const currentDuration = action.frames[index].duration;
        if (now - frameStarted >= currentDuration && index < action.frames.length - 1) {
          completedDuration += currentDuration;
          index += 1;
          frameStarted = now;
          $('transition-image').src = action.frames[index].url;
        }
        const held = Math.min(now - frameStarted, action.frames[index].duration);
        elapsed = completedDuration + held;
        finished = index === action.frames.length - 1 && held >= action.frames[index].duration;
      } else {
        elapsed = Math.min(now - started, action.duration);
        finished = elapsed >= action.duration;
      }
      $('transition-progress').style.transform = `scaleX(${elapsed / action.duration})`;
      $('frame-status').textContent = `${action.frames.length ? `第 ${index + 1}／${action.frames.length} 格 · ` : ''}${(elapsed / 1000).toFixed(1)}／${(action.duration / 1000).toFixed(1)} 秒`;
      if (!finished) raf = requestAnimationFrame(tick);
      else {
        $('frame-status').textContent = '過場播放完成';
        if (params.get('showcase') === action.id) closingTimer = setTimeout(() => play(action), 550);
        else closingTimer = setTimeout(closeTransition, 250);
      }
    }
    raf = requestAnimationFrame(tick);
  }

  function openTransition(action, trigger) {
    stopPlayback(); current = action; returnFocus = trigger || document.activeElement;
    $('transition-title').textContent = action.title;
    $('transition-visual').style.aspectRatio = action.aspectRatio;
    $('transition-category').textContent = action.category;
    $('transition-description').textContent = action.description;
    $('transition-visual').classList.remove('is-portrait');
    $('transition-progress-track').hidden = false;
    $('replay-button').hidden = false;
    $('close-dialog').setAttribute('aria-label', '略過過場並關閉');
    if (!dialog.open) dialog.showModal();
    document.body.style.overflow = 'hidden';
    $('skip-button').focus({ preventScroll: true });
    play(action);
  }

  $('featured-play').addEventListener('click', event => featured && openTransition(featured, event.currentTarget));
  $('skip-button').addEventListener('click', closeTransition);
  $('close-dialog').addEventListener('click', closeTransition);
  $('replay-button').addEventListener('click', () => current && play(current));
  dialog.addEventListener('cancel', event => { event.preventDefault(); closeTransition(); });
  dialog.addEventListener('click', event => { if (event.target === dialog) {
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) closeTransition();
  } });
  motion.addEventListener('change', () => current && dialog.open && play(current));
  if (params.has('showcase')) document.body.classList.add('showcase');

  getManifest().then(manifest => {
    const list = Array.isArray(manifest.actions) ? manifest.actions : Object.entries(manifest.actions || {}).map(([id, value]) => ({ id, ...value }));
    actions = list.map(normalize).filter(Boolean);
    if (!actions.length) throw new Error('清單中尚無可播放的實際影格。');
    const selected = actions.find(a => a.id === (params.get('showcase') || params.get('action') || 'write_brief')) || actions[0];
    selectFeatured(selected); renderFilters(); renderCards();
    $('action-tab-count').textContent = actions.length;
    renderCharacterSheets(); renderEnvironments(); loadCharacters(manifest);
    const view = params.get('view') || (['characters', 'environments'].includes(params.get('showcase')) ? params.get('showcase') : 'actions');
    if (view !== 'actions') selectView(view);
    const requestedAction = params.get('showcase') || params.get('action');
    if (actions.some(action => action.id === requestedAction)) openTransition(selected, $('featured-play'));
    window.animationPreview = { get actions() { return actions; }, select: id => { const a = actions.find(x => x.id === id); if (a) selectFeatured(a); }, play: id => { const a = actions.find(x => x.id === id); if (a) openTransition(a, $('featured-play')); }, close: closeTransition };
  }).catch(error => {
    $('library-count').textContent = '尚未載入素材';
    $('stage-empty').textContent = '請先建立完整素材包';
    $('load-message').hidden = false;
    $('load-message').textContent = `${error.message} 若直接開啟檔案，請先執行 build_preview.py；或由素材包上層啟動本機 HTTP 伺服器。`;
  });
})();
