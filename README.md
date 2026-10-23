# 訴訟之神之路

以 PDF 概念圖的人物、服裝、材質與光色為依據的 **2D 靜態動作插畫展示**。每個動作使用一張圖片，分為男性與女性主角版本；取消動畫播放與自動換幀。跳槽暫不製作動作圖，沒有音樂或音訊。

## 直接查看

1. [下載本次新增素材包 v0.4](releases/New_Art_Pack_v0.4.zip)，解壓後開啟根目錄 `index.html`。
2. 包內只有本次新增的 **31 張靜態 PNG**：男女各 14 張動作圖、剛才生成的下班家中場景 1 張、勝訴／敗訴視窗各 1 張。點圖片可看原圖，沒有收錄舊素材或音訊。
3. 完整專案另有 [動作視窗檢視器](assets/concept_v3/preview/index.html)，可選男／女主角，點動作並以「繼續」、關閉或 Esc 返回。使用 Godot 時開啟根目錄 [project.godot](project.godot) 並按 **F5**；此程式展示與舊人物圖庫不放入這次的素材 ZIP。

GitHub 的 HTML 檔案頁顯示原始碼，請下載後再開啟檢視器。單張 PNG 位於 `assets/concept_v3/action_stills/male/` 與 `female/`，也能直接開啟。

## 內容與範圍

- **14 種動作 × 男女版本，共 28 張已完成的單圖**：早餐、寫狀、摸魚、面試、查資料、拍馬屁、健身、脫口秀、法律影片、睡覺、節目、新聞採訪、諮詢、分案。清單見 [manifest.json](assets/concept_v3/manifest.json)。
- **新增家中場景與勝敗視窗**：見 [本次素材說明](assets/concept_v4/README.zh-TW.md) 與 [31 張清單](assets/concept_v4/manifest.json)。
- **專案保留的舊素材**：52 張透明人物立繪及舊背景仍可在完整專案查看；本次 ZIP 不包含它們。
- **來源與驗證**：保留靜態插畫生成提示、PNG 原圖、圖像引用及檢查報告；目前主流程不使用影片、動態 WebP、逐格序列或計時播放。

這個專案展示實際插畫與單圖視窗，尚未串接完整疲勞、金錢、案件及存檔系統。人物目前是獨立立繪，尚未完成所有可換裝圖層與骨架。

## 文件與重建

- [素材使用說明](assets/concept_v3/README.zh-TW.md)
- [Godot 單圖視窗與執行說明](godot_demo/README.zh-TW.md)
- [現行 GDD／PRD](docs/GAME_DESIGN_PRD.zh-TW.md)
- [v0.4 美術方向](docs/art/ART_DIRECTION_v3.zh-TW.md)

個別圖片及程式完成後，從根目錄執行 `python3 tools/package_static_v4.py` 產生新版下載包；加 `--check` 可檢查包內檔案與目前來源一致。

[舊 v0.3 動畫 ZIP](releases/Illustrated_Art_Action_Cutscenes_v0.3.zip) 保留作歷史回溯，不是目前的動作表現。舊 PDF／Word／CSV 設計資料保留於 `docs/`。資料夾 `assets/concept_v3` 與美術說明檔名沿用既有路徑，內文和當前清單版本已更新為 v0.4。
