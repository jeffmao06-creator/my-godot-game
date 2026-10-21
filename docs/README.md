# 訴訟之神之路｜設計與美術成果

遊戲名稱為《訴訟之神之路》。本資料夾保存贊助介紹提案，以及先前以《律師事務所模擬器》為暫名製作的完整遊戲設計文件、22 頁視覺簡報、17 頁美術清單、可編輯 Word、CSV 派工清單與四張概念圖。音樂與其他音訊不在本次交付範圍。

## 最新：贊助介紹提案（單一 PDF）

- **[《訴訟之神之路》贊助提案 PDF（24 頁）](presentation/訴訟之神之路_贊助提案.pdf)**
- 以故事、角色與世界觀介紹遊戲，聚焦贊助合作想像，不列數值、製作參數或實作規格。
- 新增九張概念圖板，包含更多角色與換裝、事務所白天／午後／夜間、下班回家的住處、休閒生活、客戶故事與合作情境；全部內嵌於這一份 PDF。
- 只使用遊戲名稱，不加入製作人姓名、團隊或個人聯絡資料；圖像為概念示意，不是實機畫面。

## 第一版設計與美術成果包

- **[第一版完整成果 ZIP](Law_Firm_Simulator_Art_Package.zh-TW.zip)**：包含原始 PRD、22 頁簡報、17 頁清單、Word、CSV、四張概念圖、來源及校驗清單，含 39 頁合併 PDF。最新贊助提案 PDF 請由上方單獨下載，不包含在這份第一版 ZIP。
- **[完整提案 PDF（39 頁）](presentation/Law_Firm_Simulator_Complete_Proposal.zh-TW.pdf)**：22 頁簡報加 17 頁完整美術清單，適合直接閱讀與分享。

在 GitHub 開啟 ZIP 或 PDF 後，點右上角 **Download raw file**（下載原始檔）或 **View raw**。大型檔案無法預覽時，仍可下載原始檔。

目前成果分支為 `docs/law-firm-design-and-art`。若要下載整個專案，先切換到這個分支，再點 **Code → Download ZIP**；下載後開啟其中的 `docs/`。從 `main` 下載不會包含尚未合併的成果分支內容。

## 文件與清單

| 成果 | 檔案 |
|---|---|
| 遊戲設計 GDD／PRD | [GAME_DESIGN_PRD.zh-TW.md](GAME_DESIGN_PRD.zh-TW.md) |
| 完整提案 PDF，39 頁 | [Law_Firm_Simulator_Complete_Proposal.zh-TW.pdf](presentation/Law_Firm_Simulator_Complete_Proposal.zh-TW.pdf) |
| 獨立視覺簡報 PDF，22 頁 | [Law_Firm_Simulator_Art_Pitch.zh-TW.pdf](presentation/Law_Firm_Simulator_Art_Pitch.zh-TW.pdf) |
| 可編輯 Word 簡報 | [Law_Firm_Simulator_Art_Pitch.zh-TW.docx](presentation/Law_Firm_Simulator_Art_Pitch.zh-TW.docx) |
| 完整美術清單 PDF，17 頁 | [Art_Production_Inventory.zh-TW.pdf](art/Art_Production_Inventory.zh-TW.pdf) |
| 可編輯 Word 美術清單 | [Art_Production_Inventory.zh-TW.docx](art/Art_Production_Inventory.zh-TW.docx) |
| CSV 派工清單，113 個唯一項目 | [ART_ASSET_LIST.csv](art/ART_ASSET_LIST.csv) |
| 美術設定與清單說明 | [ART_ASSET_LIST.zh-TW.md](art/ART_ASSET_LIST.zh-TW.md) |

CSV 使用 UTF-8 BOM，方便以 Excel 或其他試算表工具開啟。Word 建議使用 Noto Sans CJK TC 字型；需要固定版面時，優先閱讀已嵌入字型的 PDF。

## 四張概念圖

| 圖片 | 原始 PNG |
|---|---|
| 臺北事務所 | [01_taipei_office.png](presentation/assets/01_taipei_office.png) |
| 人物與服裝設定 | [02_character_sheet.png](presentation/assets/02_character_sheet.png) |
| 臺北、臺中、高雄分所 | [03_city_branches.png](presentation/assets/03_city_branches.png) |
| 辦公物件、圖示與事件氣氛 | [04_props_and_moods.png](presentation/assets/04_props_and_moods.png) |

圖像為 AI 生成的概念參考；正式 32×48 精靈、逐格動畫與地圖格仍依清單製作，不能把概念稿直接視為完成的遊戲素材。

## 可重建來源與完整性

- [簡報內容 JSON](presentation/deck_content.json)
- [簡報生成程式](presentation/build_deck.py)
- [概念圖生成提示及用途](presentation/concept_prompts.json)
- [簡報交付與重建說明](presentation/README.zh-TW.md)
- [SHA256SUMS](SHA256SUMS)：校驗個別成果與來源檔，不包含校驗清單自身及 ZIP，避免循環相依。

在 `docs/` 執行 `sha256sum -c SHA256SUMS` 可檢查檔案是否與這次交付一致。ZIP 是相同個別檔案的額外打包，解壓後也可在包內資料夾執行相同檢查。
