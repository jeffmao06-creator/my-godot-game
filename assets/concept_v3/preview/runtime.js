(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const rootURL = new URL('../', location.href);
  const params = new URLSearchParams(location.search);
  const variantLabels = { male: '男性主角', female: '女性主角' };
  const characterGroups = { protagonist: '主角外觀', player: '主角外觀', main: '主角外觀', staff: '事務所員工', employee: '事務所員工', candidate: '招募候選', recruit: '招募候選' };
  const categoryLabels = { daily: '工作日常', work: '工作日常', evening: '下班生活', leisure: '下班生活', event: '人與機會', events: '人與機會', management: '事務所經營' };
  let actions = [];
  let featured = null;
  let filter = '全部';
  let variant = params.get('gender') === 'female' ? 'female' : 'male';
  let currentAction = null;
  let characterAssets = [];
  let characterFilter = '全部角色';
  let imageRequest = 0;
  let returnFocus = null;
  const dialog = $('artwork-dialog');
  const asset = path => new URL(path, rootURL).href;

  function imagePath(value) {
    return typeof value === 'string' ? value : value?.file || value?.image || value?.path || value?.src;
  }

  function normalize(raw, index) {
    const male = imagePath(raw.images?.male);
    const female = imagePath(raw.images?.female);
    if (!raw.id || !male || !female) throw new Error('每個動作都需要男性與女性靜態圖片：' + (raw.id || index));
    return {
      id: String(raw.id), title: raw.title || raw.name || raw.id,
      description: raw.description || '', category: categoryLabels[raw.category] || raw.category || '動作插畫',
      images: { male: asset(male), female: asset(female) }, index,
    };
  }

  async function getManifest() {
    if (location.protocol === 'file:' && window.CONCEPT_MANIFEST) return window.CONCEPT_MANIFEST;
    try {
      const response = await fetch(new URL('manifest.json', rootURL), { cache: 'no-store' });
      if (!response.ok) throw new Error('無法讀取素材清單');
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

  function syncVariantButtons() {
    document.querySelectorAll('[data-protagonist]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.protagonist === variant));
    });
    $('selected-variant').textContent = variantLabels[variant];
  }

  function selectFeatured(action) {
    featured = action;
    $('featured-title').textContent = action.title;
    $('featured-description').textContent = action.description;
    $('featured-category').textContent = action.category;
    $('featured-meta').textContent = variantLabels[variant] + ' · 單張插畫';
    const picture = $('featured-image');
    picture.src = action.images[variant];
    picture.alt = variantLabels[variant] + '：' + action.title;
    picture.hidden = false;
    $('stage-empty').hidden = true;
    $('featured-view').disabled = false;
    document.querySelectorAll('.action-card').forEach(card => card.classList.toggle('is-featured', card.dataset.id === action.id));
  }

  function renderCards() {
    const visible = actions.filter(action => filter === '全部' || action.category === filter);
    $('library-count').textContent = visible.length + ' 種動作 · ' + variantLabels[variant];
    $('action-grid').replaceChildren(...visible.map(action => {
      const card = document.createElement('button');
      card.type = 'button'; card.className = 'action-card'; card.dataset.id = action.id;
      card.setAttribute('aria-label', '檢視' + variantLabels[variant] + '的' + action.title + '插畫');
      const art = document.createElement('span'); art.className = 'card-art';
      const image = imageElement(action.images[variant], variantLabels[variant] + '：' + action.title);
      image.loading = 'lazy'; art.append(image);
      const content = document.createElement('span'); content.className = 'card-content';
      const line = document.createElement('span'); line.className = 'card-line';
      const title = document.createElement('strong'); title.className = 'card-title'; title.textContent = action.title;
      const number = document.createElement('span'); number.className = 'card-index'; number.textContent = String(action.index + 1).padStart(2, '0');
      line.append(title, number);
      const description = document.createElement('span'); description.className = 'card-description'; description.textContent = action.description;
      const meta = document.createElement('span'); meta.className = 'card-meta';
      const category = document.createElement('span'); category.textContent = action.category;
      const type = document.createElement('span'); type.textContent = variantLabels[variant] + ' · 靜態圖片';
      meta.append(category, type); content.append(line, description, meta); card.append(art, content);
      card.classList.toggle('is-featured', featured?.id === action.id);
      card.addEventListener('click', () => { selectFeatured(action); openAction(action, card); });
      return card;
    }));
  }

  function renderFilters() {
    $('filters').replaceChildren(...['全部', ...new Set(actions.map(action => action.category))].map(category => {
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

  function setVariant(value) {
    if (!Object.hasOwn(variantLabels, value)) return;
    const returnActionId = returnFocus?.classList.contains('action-card') ? returnFocus.dataset.id : null;
    variant = value;
    syncVariantButtons();
    if (featured) selectFeatured(featured);
    renderCards();
    if (returnActionId) returnFocus = document.querySelector('.action-card[data-id="' + CSS.escape(returnActionId) + '"]');
    if (currentAction && dialog.open) showActionImage(currentAction);
  }

  document.querySelectorAll('[data-protagonist]').forEach(button => {
    button.addEventListener('click', () => setVariant(button.dataset.protagonist));
  });

  function selectView(view, scroll = true) {
    const selected = ['actions', 'characters', 'environments'].includes(view) ? view : 'actions';
    document.querySelectorAll('.resource-tab').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === selected)));
    $('action-panel').hidden = selected !== 'actions';
    $('character-panel').hidden = selected !== 'characters';
    $('environment-panel').hidden = selected !== 'environments';
    if (scroll) $('material-navigation').scrollIntoView({ block: 'start', behavior: 'instant' });
  }

  document.querySelectorAll('.resource-tab').forEach(button => {
    button.addEventListener('click', () => selectView(button.dataset.view));
  });

  function showImage(url, title, portrait) {
    const mine = ++imageRequest;
    const picture = $('artwork-image');
    picture.onload = () => {
      if (mine !== imageRequest) return;
      $('artwork-loading').hidden = true;
      $('artwork-visual').setAttribute('aria-busy', 'false');
    };
    picture.onerror = () => {
      if (mine !== imageRequest) return;
      $('artwork-loading').hidden = false;
      $('artwork-loading').textContent = '圖片無法載入，請確認下載包包含這張素材。';
      $('artwork-visual').setAttribute('aria-busy', 'false');
    };
    $('artwork-loading').textContent = '正在載入圖片…';
    $('artwork-loading').hidden = true;
    $('artwork-visual').setAttribute('aria-busy', 'true');
    $('artwork-visual').classList.toggle('is-portrait', Boolean(portrait));
    picture.alt = title;
    picture.src = url;
    if (!picture.complete) $('artwork-loading').hidden = false;
  }

  function showActionImage(action) {
    $('artwork-title').textContent = action.title;
    $('artwork-category').textContent = action.category;
    $('artwork-description').textContent = action.description;
    $('artwork-meta').textContent = variantLabels[variant] + ' · 單張動作插畫';
    $('dialog-variants').hidden = false;
    showImage(action.images[variant], variantLabels[variant] + '：' + action.title, false);
  }

  function openAction(action, trigger) {
    currentAction = action;
    returnFocus = trigger || document.activeElement;
    showActionImage(action);
    if (!dialog.open) dialog.showModal();
    document.body.style.overflow = 'hidden';
    $('continue-button').focus({ preventScroll: true });
  }

  function openArtwork(item, trigger) {
    currentAction = null;
    returnFocus = trigger || document.activeElement;
    $('artwork-title').textContent = item.title;
    $('artwork-category').textContent = item.category;
    $('artwork-description').textContent = item.description || '';
    $('artwork-meta').textContent = item.meta || '完整原圖';
    $('dialog-variants').hidden = true;
    showImage(item.url, item.title, item.portrait);
    if (!dialog.open) dialog.showModal();
    document.body.style.overflow = 'hidden';
    $('continue-button').focus({ preventScroll: true });
  }

  function closeArtwork() {
    imageRequest += 1;
    if (dialog.open) dialog.close();
    currentAction = null;
    document.body.style.overflow = '';
    const focus = returnFocus;
    returnFocus = null;
    if (focus?.isConnected) focus.focus({ preventScroll: true });
  }

  $('featured-view').addEventListener('click', event => featured && openAction(featured, event.currentTarget));
  $('continue-button').addEventListener('click', closeArtwork);
  $('close-dialog').addEventListener('click', closeArtwork);
  dialog.addEventListener('cancel', event => { event.preventDefault(); closeArtwork(); });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) closeArtwork();
  });

  function renderCharacterCards() {
    const visible = characterAssets.filter(character => characterFilter === '全部角色' || character.group === characterFilter);
    $('character-count').textContent = visible.length + ' 張完整立繪' + (characterFilter === '全部角色' ? '' : ' · ' + characterFilter);
    $('character-grid').replaceChildren(...visible.map(character => {
      const card = document.createElement('button'); card.type = 'button'; card.className = 'character-card';
      card.dataset.id = character.id; card.setAttribute('aria-label', '檢視' + character.title + '完整立繪');
      const art = document.createElement('span'); art.className = 'character-art';
      const image = imageElement(character.url); image.loading = 'lazy'; art.append(image);
      const caption = document.createElement('span'); caption.className = 'character-caption';
      const title = document.createElement('strong'); title.textContent = character.title;
      const label = document.createElement('small'); label.textContent = character.group;
      caption.append(title, label); card.append(art, caption);
      card.addEventListener('click', () => openArtwork({ ...character, category: character.group, portrait: true, description: '獨立透明人物立繪，保留完整身形與服裝細節。', meta: '透明 PNG' }, card));
      return card;
    }));
  }

  function renderCharacterFilters() {
    $('character-filters').replaceChildren(...['全部角色', ...new Set(characterAssets.map(character => character.group))].map(group => {
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

  async function loadCharacters(manifest) {
    let catalog = window.CONCEPT_CHARACTERS;
    if (location.protocol !== 'file:' || !catalog) {
      try {
        const response = await fetch(new URL(manifest.characters_path || 'character_catalog.json', rootURL), { cache: 'no-store' });
        if (response.ok) catalog = await response.json();
      } catch (_) { /* Offline catalog is embedded. */ }
    }
    const list = Array.isArray(catalog) ? catalog : catalog?.characters || [];
    characterAssets = list.map(item => {
      const path = item.file || item.image || item.path;
      const group = item.group || item.kind || 'protagonist';
      return path ? { id: item.id, title: item.title || item.label || item.id, url: asset(path), group: characterGroups[group] || group } : null;
    }).filter(Boolean);
    $('character-tab-count').textContent = characterAssets.length;
    renderCharacterFilters(); renderCharacterCards();
    const sheets = [
      ['主角外觀', 'characters/protagonist_variants_sheet.png'],
      ...[1, 2, 3, 4].map(number => ['人物原稿 ' + number, 'characters/staff_sheet_' + number + '.png']),
    ];
    sheets.forEach(([title, path]) => {
      const link = document.createElement('a'); link.href = asset(path); link.target = '_blank'; link.rel = 'noopener'; link.textContent = title;
      $('sheet-links').append(link);
    });
    window.assetGallery = { get characters() { return characterAssets; }, selectView };
  }

  function renderEnvironments(manifest) {
    const environments = Array.isArray(manifest.environments) && manifest.environments.length ? manifest.environments : [
      { title: '雨天辦公室', description: '雨窗、文件和暖燈，陪你度過忙碌的一天。', file: 'environments/office.png' },
      { title: '下班後的家', description: '把公事放在門邊，留一盞燈給自己。', file: 'environments/home.png' },
    ];
    $('environment-tab-count').textContent = environments.length;
    $('environment-count').textContent = environments.length + ' 個完整空間';
    $('environment-grid').replaceChildren(...environments.map(environment => {
      const path = imagePath(environment.image || environment.file || environment.path);
      const card = document.createElement('button'); card.type = 'button'; card.className = 'environment-card';
      card.setAttribute('aria-label', '檢視' + environment.title + '完整場景');
      const art = document.createElement('span'); art.className = 'environment-art';
      const image = imageElement(asset(path)); image.loading = 'lazy'; art.append(image);
      const caption = document.createElement('span'); caption.className = 'environment-caption';
      const title = document.createElement('strong'); title.textContent = environment.title;
      const description = document.createElement('small'); description.textContent = environment.description || '';
      caption.append(title, description); card.append(art, caption);
      card.addEventListener('click', () => openArtwork({ title: environment.title, description: environment.description, category: '生活場景', url: asset(path), meta: '完整場景原圖' }, card));
      return card;
    }));
  }

  getManifest().then(manifest => {
    if (Object.keys(manifest).length === 0) throw new Error('素材清單尚未建立。');
    actions = (Array.isArray(manifest.actions) ? manifest.actions : []).map(normalize);
    if (!actions.length) throw new Error('清單尚無男女版本的靜態動作圖片。');
    syncVariantButtons();
    const selected = actions.find(action => action.id === (params.get('action') || 'write_brief')) || actions[0];
    selectFeatured(selected); renderFilters(); renderCards();
    $('action-tab-count').textContent = actions.length;
    renderEnvironments(manifest); loadCharacters(manifest);
    if (params.has('showcase')) document.body.classList.add('showcase');
    if (params.has('view')) selectView(params.get('view'), false);
    window.actionArtworkPreview = {
      get actions() { return actions; }, get variant() { return variant; },
      get currentActionId() { return currentAction?.id || null; },
      select: id => { const action = actions.find(item => item.id === id); if (action) selectFeatured(action); },
      open: id => { const action = actions.find(item => item.id === id); if (action) openAction(action, $('featured-view')); },
      setVariant, close: closeArtwork,
    };
  }).catch(error => {
    $('library-count').textContent = '尚未載入素材';
    $('stage-empty').textContent = '請先下載完整靜態素材包';
    $('load-message').hidden = false;
    $('load-message').textContent = error.message;
  });
})();
