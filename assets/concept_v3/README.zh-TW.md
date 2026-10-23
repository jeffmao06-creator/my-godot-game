# 訴訟之神之路｜v0.4 男女主角靜態動作圖

本版沿用 PDF 概念圖的造型、材質及光色，以平滑輪廓的 2D 插畫呈現每個動作。**一個動作、一個主角版本，只用一張圖片。** 不製作或播放動畫，不設幀率、時長及進度條。

`assets/concept_v3` 是沿用的資料夾名稱；當前靜態版為 v0.4。v0.3 動畫保留在舊目錄、Git 歷史與舊 ZIP，不作目前主流程或本版素材。

## 看圖片

下載 [本次新增素材 ZIP](../../releases/New_Art_Pack_v0.4.zip) 後開啟根目錄 `index.html`，內含 31 張新圖，不包含舊圖庫或 Godot。完整專案另可開啟 [preview/index.html](preview/index.html)。選男性／女性主角，再點動作卡片，視窗會持續顯示該張圖；按「繼續」、關閉或 Esc 返回。未操作時不會換圖或自行關閉，沒有播放、重播或略過功能。

「人物素材」頁可查看 52 張透明立繪，「生活場景」頁可查看辦公室與住家。Godot 則開啟專案根目錄 `project.godot` 並按 F5。

## 動作範圍

| 類型 | 動作 |
|---|---|
| 日常行動 | 吃早餐、寫書狀、摸魚、面試新員工、查找資料、拍老闆馬屁 |
| 下班行動 | 健身、看脫口秀、看法律講座影片、我只想睡覺 |
| 事件／管理 | 電視節目、新聞採訪、客戶諮詢、分派案件 |

共 14 個動作，每項各製作男性與女性主角一張，共 28 張已完成 PNG，已通過尺寸、單幀與來源雜湊檢查。跳槽不在本版範圍，沒有音樂及其他音訊。

女性版本使用同一位女性主角的臉、髮型與工作／居家服，不能用同場客戶、候選或主持人充當女性主角。男女版本只影響外觀，不改能力、疲勞、金錢或成功率。

## 檔案

- [manifest.json](manifest.json)：14 個動作與 `images.male`／`images.female` 靜態 PNG 引用。
- `action_stills/male/<id>.png`：男性主角的單張動作圖。
- `action_stills/female/<id>.png`：女性主角的單張動作圖。
- [static_generation_manifest.json](static_generation_manifest.json)：本版靜態圖生成提示、來源與原圖雜湊。
- [exports/static_asset_validation.json](exports/static_asset_validation.json)：靜態圖是否存在、尺寸及男女覆蓋檢查。
- [character_catalog.json](character_catalog.json)：4 主角外觀、45 員工、3 候選共 52 張獨立透明立繪。
- `characters/`、`environments/`：沿用的人物與兩張背景。
- `preview/qa/`：靜態視窗、男女切換及圖片載入的檢查報告；QA 截圖保留在 Git 專案。

這些是單張插畫與完整立繪，不是拆好的臉、髮、衣服圖層或骨架。展示未串接經營數值、案件及存檔。未來接入主遊戲時，主流程仍需讓行動只結算一次；外觀切換、繼續或關閉視窗都不應重抽結果或再扣資源。

## 同步與封裝

```sh
python3 assets/concept_v3/preview/build_preview.py
python3 tools/package_static_v4.py
```

第一個指令同步清單供離線開啟，不生成或修改插畫。靜態圖由圖像生成工具製作，原圖與提示另行保留。封裝工具加 `--check` 可驗證下載包；Godot 以同一清單讀取單張圖片。

`SHA256SUMS` 以本目錄為基準；本次新增素材 ZIP 根目錄另有其 31 張新圖及附件的校驗表。封裝工具只收本次新增素材，完整專案的展示程式與舊人物不入包。舊 `tools/build_assets.py`／v0.3 動畫封裝流程不適用本版單圖需求。
