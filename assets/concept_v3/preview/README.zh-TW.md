# 動作過場素材檢視

此頁展示《訴訟之神之路》的實際動作影格與小視窗播放機制，不是可玩的完整遊戲。人物與動作畫面取自同一素材包，沒有用 SVG 人物或平移靜態插畫代替逐格動作。

「人物素材」可查看 4 種主角外觀、45 名員工與 3 名候選的完整透明立繪，並按類型篩選；點選人物可放大檢視。另可打開 5 張整體人物原稿。「生活場景」展示辦公室與下班住家。此處是實際素材展示，不把獨立立繪宣稱為已完成的 NPC 組裝系統。

## 開啟

素材包完成後可直接以瀏覽器開啟 `index.html`。也可以從專案根目錄執行：

```sh
python3 -m http.server 8000
```

再開啟 `http://localhost:8000/assets/concept_v3/preview/`。

點選動作卡或「播放過場」，會打開動畫小視窗；逐格播完自動收起。「略過」、關閉與 Esc 可立即停止，不會把計時器留到下一個動作。使用系統的「減少動態」偏好時，顯示靜態首格並由使用者關閉。小視窗以原生 dialog 管理鍵盤焦點，關閉後返回原按鈕。

`?showcase` 使用展示版排版；`?showcase=write_brief` 會自動打開寫書狀並循環，供錄影或截圖。一般模式播完關閉；`?action=write_brief` 只自動播放一次。

`?view=characters` 或 `?view=environments` 可直接進入人物／場景頁。

## 同步清單

```sh
python3 assets/concept_v3/preview/build_preview.py
```

程式讀取上層 `manifest.json` 與 `character_catalog.json`，寫出 `manifest_data.js`，讓下載後直接開啟也不需要 fetch 或網路。透過 HTTP 預覽時會優先讀取最新清單，避免開發時使用過期副本。圖片路徑一律相對 `assets/concept_v3/`。

每個 action 包含 `id`、`title`、`category`、`description` 與 `frames`。影格可為路徑字串或 `{src, duration_ms}`。使用明確影格時長或 `frame_durations_ms` 陣列優先；其次使用 `frame_duration_ms` 與 `last_frame_duration_ms`，再其次依整段 `duration_ms` 平分，皆沒有才依 `fps` 計時。也可提供 `poster`，否則使用第一格。預覽使用原圖比例、不採像素取樣。

2800 毫秒是素材的基準播放時間。播放器逐一保留全部姿勢；若裝置忙碌，會略延長總播放時間，而不跳過中間影格。

此檢視器不發送網路分析，不保存個人資料，不觸發遊戲數值、案件或日期變更。正式遊戲整合時，請在過場完成回呼之後結算已選定的行動，並在開啟期間阻擋重複點擊。

## Godot 展示與驗證

需要在 Godot 中檢視時，開啟專案根目錄的 [project.godot](../../../project.godot)；整合方式見 [Godot 展示說明](../../../godot_demo/README.zh-TW.md)。兩個播放器讀取同一批真實影格與時長，沒有各自製作一份外觀。

網頁驗證使用 Python Playwright 與 Chromium：

```sh
python3 assets/concept_v3/preview/validate_preview.py
```

驗證會確認完整 14 動作及 12 影格、實際前進、播放完成、略過／Esc／重播、焦點、減少動態與手機版面，以及 52 張人物 PNG 的 4／45／3 分類、靜態放大及兩張場景；`qa/` 保存來源清單雜湊與檢查報告；QA 截圖保留在 Git 專案，下載素材 ZIP 不重複打包這些介面截圖。
