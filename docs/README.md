# 訴訟之神之路｜設計與美術成果

2026-10-23 的 v0.2 修訂處理人物重複、肖像分層、場景投影與雨窗、色票、HUD 情境及時段表。音樂與所有音訊不在交付範圍。

## 閱讀與下載

- **[贊助介紹提案 PDF，24 頁](presentation/訴訟之神之路_贊助提案.pdf)**：介紹故事、角色、三城市、事務所日夜與下班住家；不列製作參數或個人聯絡資料。
- **[完整設計與美術提案 PDF，38 頁](presentation/Law_Firm_Simulator_Complete_Proposal.zh-TW.pdf)**：22 頁視覺簡報＋16 頁完整美術清單。
- **[完整成果下載包 ZIP](Law_Firm_Simulator_Art_Package.zh-TW.zip)**：含本版全部文件、贊助 PDF、原始圖、分層原型及來源；不含 ZIP 自身。
- **[v0.2 修訂與驗證紀錄](REVISION_NOTES.zh-TW.md)**：逐項對應這次修正。

GitHub 上開啟 PDF 或 ZIP 後，點 **Download raw file**（下載原始檔）或 **View raw**。成果分支為 `docs/law-firm-design-and-art`；要下載全部檔案，先切換到此分支，再點 **Code → Download ZIP**，解壓後開啟 `docs/`。`main` 在合併前不會包含此分支的修訂。

既有英文檔名為維持連結而保留，文件內正式遊戲名稱已統一為《訴訟之神之路》。

## 文件與清單

| 成果 | 檔案 |
|---|---|
| 遊戲設計 GDD／PRD | [GAME_DESIGN_PRD.zh-TW.md](GAME_DESIGN_PRD.zh-TW.md) |
| 視覺簡報 PDF，22 頁 | [Law_Firm_Simulator_Art_Pitch.zh-TW.pdf](presentation/Law_Firm_Simulator_Art_Pitch.zh-TW.pdf) |
| 可編輯 Word 簡報 | [Law_Firm_Simulator_Art_Pitch.zh-TW.docx](presentation/Law_Firm_Simulator_Art_Pitch.zh-TW.docx) |
| 美術清單 PDF，16 頁 | [Art_Production_Inventory.zh-TW.pdf](art/Art_Production_Inventory.zh-TW.pdf) |
| 可編輯 Word 美術清單 | [Art_Production_Inventory.zh-TW.docx](art/Art_Production_Inventory.zh-TW.docx) |
| CSV 派工清單，136 個唯一項目 | [ART_ASSET_LIST.csv](art/ART_ASSET_LIST.csv) |
| 美術設定、交付與驗收 | [ART_ASSET_LIST.zh-TW.md](art/ART_ASSET_LIST.zh-TW.md) |
| 共用色名、色碼、投影及臺北雨景基準 | [visual_style.json](art/visual_style.json) |
| 48 人持久外觀資料樣本 | [appearance_manifest.json](art/appearance_manifest.json) |
| 45 員工＋3 候選分層互動原型 | [index.html](art/appearance_proof/index.html)（下載後以瀏覽器開啟） |
| 分層原型使用與重建說明 | [README.zh-TW.md](art/appearance_proof/README.zh-TW.md) |

CSV 使用 UTF-8 BOM，方便以 Excel 開啟。Word 建議使用 Noto Sans CJK TC；需要固定版面時請閱讀嵌入字型的 PDF。

## 概念圖與結構原型

| 參照 | 圖片 |
|---|---|
| 臺北雨天辦公室，平行格線與窗框 | [01_taipei_office.png](presentation/assets/01_taipei_office.png) |
| 八人服裝與氣質，並非 NPC 基底庫 | [02_character_sheet.png](presentation/assets/02_character_sheet.png) |
| 臺北雨窗、臺中、高雄正交分所 | [03_city_branches.png](presentation/assets/03_city_branches.png) |
| 辦公物件與圖示造型 | [04_props_and_moods.png](presentation/assets/04_props_and_moods.png) |
| 肖像分層視覺概念，並非透明成品圖集 | [05_portrait_layer_concept.png](presentation/assets/05_portrait_layer_concept.png) |
| 45 員工＋3 候選資料驅動合成原型 | [48_roster_proof.png](art/appearance_proof/48_roster_proof.png) |
| 同一身份的圖層開關示意 | [portrait_layers_proof.png](art/appearance_proof/portrait_layers_proof.png) |

349 個繪製基底是待製作需求量，並非已交付成品張數。48 人原型使用低擬真 SVG 層檢查資料與組裝關係；正式像素人物、肖像層、逐格動畫及動作適配仍待製作。場景概念圖也不是可直接匯入的 640×360 地圖。

## 來源與完整性

- [技術簡報重建說明](presentation/README.zh-TW.md)、[內容 JSON](presentation/deck_content.json)、[生成程式](presentation/build_deck.py)
- [贊助簡報重建說明與來源](presentation/sponsor/README.zh-TW.md)
- [概念圖提示、採用範圍及退回紀錄](presentation/concept_prompts.json)
- [SHA256SUMS](SHA256SUMS)：校驗個別成果與來源，不含清單自身及 ZIP，避免循環相依。

在 `docs/` 執行 `sha256sum -c SHA256SUMS` 可驗證本版檔案。ZIP 解壓後同樣可在包內 `docs/` 執行校驗。`python3 docs/build_delivery.py` 可在個別文件匯出後重建合併 PDF、校驗表與完整 ZIP；加 `--check` 可唯讀檢查目前交付。完整專案也可透過 GitHub **Code → Download ZIP** 取得。
