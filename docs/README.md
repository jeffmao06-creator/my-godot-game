# 訴訟之神之路｜設計與美術成果

## 最新：v0.4 男女主角靜態動作圖

2026-10-23 改為**每個動作一張靜態插畫，增加女性主角版本，取消動畫**。畫風延續 PDF 概念圖的人物、材質與光色；不強制像素尺寸。範圍為 14 種動作，每種 male／female 各一張，共 28 張已完成 PNG，另新增下班家中場景與勝敗視窗，共 31 張新素材；**跳槽暫不製作動作圖**。音樂與所有音訊不在交付範圍。

- [v0.4 本次新增素材 ZIP](../releases/New_Art_Pack_v0.4.zip)：31 張新 PNG、離線圖庫與清單；解壓開根目錄 `index.html`。不包含舊素材或 Godot 專案。
- [現行 GDD／PRD](GAME_DESIGN_PRD.zh-TW.md)：v0.4 單圖與男女版本需求。
- [v0.4 美術方向與範圍](art/ART_DIRECTION_v3.zh-TW.md)：畫面、主角身份、14 項動作與驗收。
- [開啟靜態動作圖檢視器](../assets/concept_v3/preview/index.html)／[使用說明](../assets/concept_v3/preview/README.zh-TW.md)：下載後選擇男／女主角，點動作顯示一張圖片，以繼續、關閉或 Esc 返回。
- [Godot 展示](../godot_demo/README.zh-TW.md)：用 Godot 開啟根目錄 `project.godot`，按 F5。
- [實際素材清單](../assets/concept_v3/manifest.json)／[靜態素材驗證](../assets/concept_v3/exports/static_asset_validation.json)：以可用圖片與缺項判斷完成範圍，不把規格張數當成完成數。

視窗不播放、不輪播、不自動換圖或關閉；男女切換只影響外觀。沿用 52 張透明立繪與兩張背景，尚未串接完整疲勞、金錢、案件及存檔系統，也不宣稱 NPC 的可換裝骨架已完成。

資料夾 `assets/concept_v3` 與美術說明檔名沿用舊路徑，當前內容版本為 v0.4。[舊 v0.3 動畫 ZIP](../releases/Illustrated_Art_Action_Cutscenes_v0.3.zip) 保留原樣供歷史回溯，不是目前動作表現。以下 PDF、Word、CSV、SVG 與設計文件 ZIP 為 v0.2 歷史資料；現行 GDD 已更新至 v0.4。

## v0.2 歷史文件與下載

- **[贊助介紹提案 PDF，24 頁](presentation/訴訟之神之路_贊助提案.pdf)**：介紹故事、角色、三城市、事務所日夜與下班住家；不列製作參數或個人聯絡資料。
- **[完整設計與美術提案 PDF，38 頁](presentation/Law_Firm_Simulator_Complete_Proposal.zh-TW.pdf)**：22 頁視覺簡報＋16 頁完整美術清單。
- **[v0.2 歷史設計文件 ZIP](Law_Firm_Simulator_Art_Package.zh-TW.zip)**：保留當時 PDF、Word、CSV、概念圖與 SVG 原型；不包含目前的靜態動作圖、HTML 或 Godot 專案。
- **[v0.2 修訂與驗證紀錄](REVISION_NOTES.zh-TW.md)**：逐項對應這次修正。

GitHub 上開啟 PDF 或 ZIP 後，點 **Download raw file**（下載原始檔）或 **View raw**。成果分支為 `docs/law-firm-design-and-art`；要下載全部檔案，先切換到此分支，再點 **Code → Download ZIP**，解壓後開啟 `assets/concept_v3/preview/` 查看新版靜態動作圖，或開啟 `docs/` 閱讀文件。`main` 在合併前不會包含此分支的修訂。

既有英文檔名為維持連結而保留，文件內正式遊戲名稱已統一為《訴訟之神之路》。

## v0.2 文件與清單（GDD 已更新）

| 成果 | 檔案 |
|---|---|
| 遊戲設計 GDD／PRD | [GAME_DESIGN_PRD.zh-TW.md](GAME_DESIGN_PRD.zh-TW.md) |
| 視覺簡報 PDF，22 頁 | [Law_Firm_Simulator_Art_Pitch.zh-TW.pdf](presentation/Law_Firm_Simulator_Art_Pitch.zh-TW.pdf) |
| 可編輯 Word 簡報 | [Law_Firm_Simulator_Art_Pitch.zh-TW.docx](presentation/Law_Firm_Simulator_Art_Pitch.zh-TW.docx) |
| 美術清單 PDF，16 頁 | [Art_Production_Inventory.zh-TW.pdf](art/Art_Production_Inventory.zh-TW.pdf) |
| 可編輯 Word 美術清單 | [Art_Production_Inventory.zh-TW.docx](art/Art_Production_Inventory.zh-TW.docx) |
| CSV 派工清單，136 個唯一項目 | [ART_ASSET_LIST.csv](art/ART_ASSET_LIST.csv) |
| 美術設定、交付與驗收 | [ART_ASSET_LIST.zh-TW.md](art/ART_ASSET_LIST.zh-TW.md) |
| v0.2 色名、投影及雨景登錄，僅供舊 PDF 重建 | [visual_style.json](art/visual_style.json) |
| 48 人持久外觀資料樣本 | [appearance_manifest.json](art/appearance_manifest.json) |
| v0.2 低擬真分層結構原型，非現行美術 | [index.html](art/appearance_proof/index.html)（下載後以瀏覽器開啟） |
| 分層原型使用與重建說明 | [README.zh-TW.md](art/appearance_proof/README.zh-TW.md) |

CSV 使用 UTF-8 BOM，方便以 Excel 開啟。Word 建議使用 Noto Sans CJK TC；需要固定版面時請閱讀嵌入字型的 PDF。

## v0.2 概念圖與結構原型（歷史）

| 參照 | 圖片 |
|---|---|
| 臺北雨天辦公室，平行格線與窗框 | [01_taipei_office.png](presentation/assets/01_taipei_office.png) |
| 八人服裝與氣質，並非 NPC 基底庫 | [02_character_sheet.png](presentation/assets/02_character_sheet.png) |
| 臺北雨窗、臺中、高雄正交分所 | [03_city_branches.png](presentation/assets/03_city_branches.png) |
| 辦公物件與圖示造型 | [04_props_and_moods.png](presentation/assets/04_props_and_moods.png) |
| 肖像分層視覺概念，並非透明成品圖集 | [05_portrait_layer_concept.png](presentation/assets/05_portrait_layer_concept.png) |
| 45 員工＋3 候選資料驅動合成原型 | [48_roster_proof.png](art/appearance_proof/48_roster_proof.png) |
| 同一身份的圖層開關示意 | [portrait_layers_proof.png](art/appearance_proof/portrait_layers_proof.png) |

v0.2 的 349 個繪製基底是當時待製作需求量，並非成品張數；其低擬真 SVG 只檢查資料與組裝關係，不代表本版插畫品質。舊概念圖也不是可直接匯入的地圖；現行素材與單圖視窗請以上方 v0.4 入口為準。

## 歷史文件來源與完整性

- [技術簡報重建說明](presentation/README.zh-TW.md)、[內容 JSON](presentation/deck_content.json)、[生成程式](presentation/build_deck.py)
- [贊助簡報重建說明與來源](presentation/sponsor/README.zh-TW.md)
- [概念圖提示、採用範圍及退回紀錄](presentation/concept_prompts.json)
- [SHA256SUMS](SHA256SUMS)：校驗個別成果與來源，不含清單自身及 ZIP，避免循環相依。

專案內 `docs/SHA256SUMS` 已更新為目前文件的校驗；v0.2 歷史 ZIP 內的校驗表則對應當時快照，兩者各自使用。`docs/build_delivery.py` 是舊 PDF 文件管線，新版請使用 `python3 tools/package_static_v4.py`；加 `--check` 可檢查新版 ZIP 與來源一致。若要取得包含歷史文件的整個專案，使用 GitHub **Code → Download ZIP**。
