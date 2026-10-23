# 訴訟之神之路｜視覺簡報交付包

v0.2 為 22 頁、16:9、繁體中文視覺簡報，Word 與 PDF 使用相同內容來源；另提供 24 頁、以故事與合作想像為主的[贊助介紹提案](訴訟之神之路_贊助提案.pdf)。不包含音樂或其他音訊。

## 檔案用途

| 檔案 | 用途 |
|---|---|
| [主簡報 PDF](Law_Firm_Simulator_Art_Pitch.zh-TW.pdf) | 固定版面的閱讀與分享版本 |
| [可編輯 Word](Law_Firm_Simulator_Art_Pitch.zh-TW.docx) | 可編輯文字、表格與概念圖 |
| [合併提案 PDF](Law_Firm_Simulator_Complete_Proposal.zh-TW.pdf) | 22 頁簡報＋16 頁清單，共 38 頁 |
| [美術規格 Markdown](../art/ART_ASSET_LIST.zh-TW.md) | 圖層、尺寸、動畫、相容性、交付及驗收 |
| [CSV](../art/ART_ASSET_LIST.csv) | 136 個工作項目，UTF-8 BOM 編碼 |
| [清單 Word](../art/Art_Production_Inventory.zh-TW.docx)／[PDF](../art/Art_Production_Inventory.zh-TW.pdf) | 完整詳細規格 |
| [GDD／PRD](../GAME_DESIGN_PRD.zh-TW.md) | 玩法、經濟與 39 項開發驗收條件 |
| [48 人分層原型](../art/appearance_proof/index.html) | 下載後離線開啟，逐人檢視肖像、小人及圖層 |

## 本版參照

- `assets/01_taipei_office.png`：取代舊透視黃昏圖，採平行格線、矩形桌面與臺北雨窗。
- `assets/02_character_sheet.png`：只作服裝與氣質參考；八人插圖不是 NPC 基底庫或固定職級身體。
- `assets/03_city_branches.png`：三城市共用正交相機，臺北使用雨灰窗景。
- `assets/04_props_and_moods.png`：沿用檔名，更新為物件與圖示，不再含舊透視場景小稿。
- `assets/05_portrait_layer_concept.png`：新分層視覺方向，不是透明圖層成品。
- 第 12 頁使用 `../art/appearance_proof/48_roster_wide.png`，標為結構原型，與離線檢視頁面同源。

概念原圖以完整比例置入，不是正式 640×360 場景或精靈表；圖中桌數也不是十五員工席位的容量驗收。提示、被替換及退回原因見 [concept_prompts.json](concept_prompts.json)。

## 數量與規則來源

清單為 **136 個工作項目、349 個待製作繪製基底**。人物改為 10 類精靈層／93 個造型與 13 類肖像層／122 個造型；18 個職務配置不計新圖，配色不計新造型。8 身形×48 為 384 個基礎身體 pose 槽位，衣髮、配件及動作適配另驗收，不能把 384 當全部成品影格。

生成程式從 CSV 計算總數，從 [visual_style.json](../art/visual_style.json) 讀取唯一色名及色碼，從 JSON 共用資料產生行動矩陣及 HUD。受僱／合署在 09／13／16 都可跳槽，開業在同三時段都可面試。

HUD 採首日 1 月 1 日 09:00：50,000、疲勞 100／100，一件教學案於晨扣後剛分派；今日負擔 0，明早預計 0.9。未經月結或支出，特性不減疲勞。這是可成立的設計情境，並非遊戲實機存檔。

## 重建

依賴 Python 3、reportlab、python-docx、fonttools 與 Noto Sans CJK TC；PDF 內嵌所需字型子集。建議優先閱讀 PDF，以免 Word 替代字型改變換行。

```sh
cd docs/presentation
python3 build_deck.py --content deck_content.json --out-dir . --prefix Law_Firm_Simulator_Art_Pitch.zh-TW
```

美術清單由 `../art/build_inventory.py` 重建；贊助版指令見 [sponsor/README.zh-TW.md](sponsor/README.zh-TW.md)。這些程式只製作文件與檢視原型，沒有實作遊戲邏輯。經濟及 NPC 過勞等建議初值仍需後續平衡試玩。

個別文件全部匯出後，從專案根目錄執行 `python3 docs/build_delivery.py`，即可重建 38 頁合併 PDF、整份 docs 校驗清單及完整下載包。
