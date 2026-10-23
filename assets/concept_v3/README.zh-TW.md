# 訴訟之神之路｜v0.3 插畫素材與動作過場

本版以 PDF 概念圖的造型、材質及光色為依據，使用平滑輪廓的 2D 插畫，取消強制像素尺寸。實際生成圖像保留於 `raw/sheets/`、`characters/`、`environments/`；舊 SVG 結構原型不作本版美術。

## 看成果

下載整包後開啟 [preview/index.html](preview/index.html)。點動作卡片可播放小視窗，按略過、關閉或 Esc 可返回；播完也會自動關閉。人物與場景頁可查看新立繪和兩個背景。Godot 則開啟專案根目錄 `project.godot` 並按 F5。

每支動畫也提供 `actions/<id>/preview.webp` 與 `preview.mp4`。兩者皆無聲；WebP 可由支援的瀏覽器開啟，MP4 可由一般影片播放器開啟。

## 素材範圍

| 類型 | 本版內容 |
|---|---|
| 日常行動 | 吃早餐、寫書狀、摸魚、面試新員工、查找資料、拍老闆馬屁 |
| 下班行動 | 健身、看脫口秀、看法律講座影片、我只想睡覺 |
| 事件／管理 | 電視節目、新聞採訪、客戶諮詢、分派案件 |
| 人物 | 4 個主角工作／居家外觀、45 員工＋3 候選人的獨立透明立繪 |
| 場景 | 雨天辦公室、雨夜住家 |

跳槽不製作過場。完整立繪不是已拆好的臉、髮、衣服與骨架；本版動畫以預設男性主角演出，女性立繪已提供，其他主角外觀的動作替換仍需補製。沒有音樂與其他音訊。

## 檔案與播放

- [manifest.json](manifest.json)：14 支實際動畫的檔案、尺寸與逐幀時間。
- [character_catalog.json](character_catalog.json)：52 張獨立人物的 ID、來源與切出範圍。
- [generation_manifest.json](generation_manifest.json)：生成提示、參照、原圖雜湊及早餐修正紀錄。
- `raw/sheets/`：14 張完整 4×3 動作原稿；`raw/references/` 的早餐初稿只作風格參照。
- `actions/<id>/frame_01.png` 至 `frame_12.png`：12 個實繪姿勢幀，單幀 478×267。一般幀 200ms、末幀 600ms，共 2.8 秒。
- `actions/<id>/slice_map.json`：每幀從原稿切出的確切座標。
- `characters/`：完整透明原稿及獨立立繪；`environments/`：兩個背景。
- `exports/asset_validation.json`、人物切圖驗證、`preview/qa/`：實際檔案與播放檢查。

動畫採有限逐格插畫表現，具有實際的手臂、表情與道具姿勢變化；不是 24fps 骨架或影片生成結果。小窗播放元件提供完成回呼，後續串接遊戲時應以獨立行動交易完成一次結算，動畫略過不再計算金錢／疲勞。現有展示沒有經營數值或存檔系統。

## 重新封裝

```sh
python3 assets/concept_v3/tools/build_assets.py
python3 assets/concept_v3/tools/cut_characters.py
python3 assets/concept_v3/preview/build_preview.py
python3 tools/package_concept_v3.py
```

第一步只切分已生成的原稿並轉檔，不重新生成圖像；需要 Python、Pillow、NumPy、SciPy、FFmpeg、ImageMagick。瀏覽器自動檢查另需 Playwright 與 Chromium，Godot 展示使用 Godot 4。完整提示與原稿保留，人物分離只處理透明區及相鄰人物，不重畫身體或改變原圖的姿勢。

素材 ZIP 收錄全部新原稿、素材與播放程式及 JSON 檢查報告；重複顯示素材的 QA 介面截圖保留在 Git 專案。

本目錄的 `SHA256SUMS` 以本目錄為基準，涵蓋實際打包檔案（不含 QA 截圖）；解壓完整下載包後，包根目錄另有整包個別檔案的 `SHA256SUMS`。封裝工具 `--check` 會確認 ZIP 沒有漏檔或混用舊圖。
