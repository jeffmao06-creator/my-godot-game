# 訴訟之神之路

依 PDF 概念圖的人物、服裝、材質與光色重做的 **2D 插畫素材與動作過場展示**，不再強制像素畫。包含辦公室、下班住家、透明人物立繪，以及 14 種小視窗逐格短動畫；跳槽暫不製作動畫。沒有音樂或音訊。

## 直接查看

1. [下載 v0.3 素材與可運行展示 ZIP](releases/Illustrated_Art_Action_Cutscenes_v0.3.zip)，解壓後開啟 `assets/concept_v3/preview/index.html`。
2. 在瀏覽器選一項動作，即可播放、略過或關閉小視窗；另可查看人物與兩個場景。
3. 使用 Godot 時，開啟根目錄 [project.godot](project.godot)，按 **F5**。可切換「事務所／回到家」背景。

也可直接開啟 `assets/concept_v3/actions/<動作ID>/preview.webp` 或 `preview.mp4` 看動畫。GitHub 的 HTML 檔案頁顯示原始碼，請下載後再開啟檢視器。

## 內容

- **14 段動畫、168 個繪製姿勢幀**：早餐、寫狀、摸魚、面試、查資料、拍馬屁、健身、脫口秀、法律影片、睡覺、節目、新聞採訪、諮詢、分案。
- **人物與場景素材**：男女主角的工作／居家立繪、45 名員工與 3 名候選人的透明立繪、辦公室與雨夜住家背景；獨立檔案清單見 [character_catalog.json](assets/concept_v3/character_catalog.json)。
- **來源與驗證**：保留生成原稿、提示、切圖座標、PNG 影格、動態 WebP、無聲 MP4、播放程式及檢查報告。

這個可運行專案用來看實際美術與過場，尚未串接完整的疲勞、金錢、案件及存檔系統。人物目前是獨立立繪，尚未完成所有可換裝圖層、骨架與走路動畫。

## 文件與重建

- [素材使用說明](assets/concept_v3/README.zh-TW.md)
- [Godot 過場元件與執行說明](godot_demo/README.zh-TW.md)
- [現行 GDD／PRD](docs/GAME_DESIGN_PRD.zh-TW.md)
- [v0.3 美術方向](docs/art/ART_DIRECTION_v3.zh-TW.md)

所有個別檔案完成後，從根目錄執行 `python3 tools/package_concept_v3.py` 產生新版下載包；加 `--check` 可檢查包內檔案與目前來源一致。下載包只收錄新版素材、展示程式及現行設計說明；舊 PDF／Word／CSV 的歷史設計資料保留於 GitHub 專案的 `docs/`。
