# 律師事務所模擬器｜視覺簡報交付包

本次將既有 PRD 整理為 **22 頁、16:9、繁體中文視覺簡報**，搭配四張 2D 像素風概念圖與完整美術製作清單。**不包含音樂或其他音訊製作。**

## 先開哪些檔案

| 檔案 | 用途 |
|---|---|
| [主簡報 PDF](Law_Firm_Simulator_Art_Pitch.zh-TW.pdf) | 保留設計版面的檢閱、分享與提案版本 |
| [可編輯 Word](Law_Firm_Simulator_Art_Pitch.zh-TW.docx) | 文字、表格與概念圖可編輯；排版依使用的 Word／字型可能略有差異 |
| [完整資源清單 Markdown](../art/ART_ASSET_LIST.zh-TW.md) | 美術方向、尺寸、動畫、命名、交付與驗收 |
| [可派工 CSV](../art/ART_ASSET_LIST.csv) | Excel／試算表可開啟，UTF-8 BOM 編碼 |
| [完整清單 Word](../art/Art_Production_Inventory.zh-TW.docx) | 可編輯的詳細規格報告 |
| [完整清單 PDF](../art/Art_Production_Inventory.zh-TW.pdf) | 詳細規格與資源表的閱讀版本 |
| [原始 PRD](../GAME_DESIGN_PRD.zh-TW.md) | 玩法、經濟公式與 34 項開發驗收條件 |
| [簡報內容來源](deck_content.json) | 後續重排與更新文字的結構化資料 |

## 四張概念圖

1. [臺北事務所](assets/01_taipei_office.png)：文件堆、暖燈、臺北夜景與工作壓力。
2. [人物設定](assets/02_character_sheet.png)：男女主角、老闆、律師及客戶，含服裝與小比例參考。
3. [三城市分所](assets/03_city_branches.png)：臺北藍灰、臺中暖日、高雄港灣；共用家具與不同窗景。
4. [物件與事件氣氛](assets/04_props_and_moods.png)：辦公設備、圖示方向、加班與休息的情緒小稿。

圖像由 image_gen 生成，屬美術定調與構圖參考，**不是已完成的遊戲場景、透明精靈或逐格動畫**。大人物是服裝設計參考，正式人物仍依 32×48、約三頭身、腳點 (16,44) 重製。概念圖的桌數不是最終十五席配置。圖像來源提示保留於 [concept_prompts.json](concept_prompts.json)。

## 製作清單摘要

- 113 個工作項目、179 個分類基底。
- 15 個場景版型，場景光線與佈置可重用。
- 18 個人物精靈基底，共 704 個動畫影格槽位。
- 18 肖像基底、108 表情輸出。
- 23 道具、14 UI 模板、48 一般圖示、13 特性圖示。
- 二十個存檔位共用一套槽位模板，不需二十張不同圖片。
- 正式遊戲素材目前均標示「待製作」，不是已交付 179 張成品。

基底、變體、影格與檔案數是不同單位；清單總數供追蹤，不可直接拿來以單張均價估整體工時。

## 編輯與重建

推薦閱讀 PDF；編輯 Word 時建議安裝 **Noto Sans CJK TC**，避免系統替代字型改變換行。

簡報生成依賴 Python 3、reportlab、python-docx、fonttools，以及已安裝的 Noto CJK TC 字型。使用的 Noto CJK 字型依 SIL Open Font License 1.1 提供；PDF 內嵌文件所需字型子集，原始字型不隨包另行轉售。

```sh
cd docs/presentation
python3 build_deck.py \
  --content deck_content.json \
  --out-dir . \
  --prefix Law_Firm_Simulator_Art_Pitch.zh-TW
```

生成腳本只讀取文字與概念圖片，不會實作或修改遊戲邏輯。原始圖片以完整比例置入，沒有把人物或場景裁成可用精靈。

## 玩法對齊

保留「疲勞與金錢管理」核心；主角自由選一金一銀，受僱／合署／開業、三城市、每所十五名受僱律師、四時段及二十存檔位均沿用 PRD。委任費、補足的一般民事 10%、NPC 過勞細則等新增值仍屬建議初值，不宣稱已完成遊戲平衡試玩。
