# 《訴訟之神之路》贊助概念簡報來源

本資料夾保存 24 頁贊助概念簡報的文案、排版程式與原始概念圖。成品是上層的 [訴訟之神之路_贊助提案.pdf](../訴訟之神之路_贊助提案.pdf)。

這份簡報以角色、臺灣城市、工作與生活的情境介紹遊戲，供合作交流使用。圖像均為開發中概念；人物插畫不是完成的角色圖集，插畫人數也不代表正式 NPC 的人數或外觀上限。正式 NPC 的分層外觀需求另見 [美術清單](../../art/ART_ASSET_LIST.zh-TW.md)。

## 共用來源

- `sponsor_content.json`：24 頁繁體中文文案、版型及圖片引用。
- `build_sponsor_deck.py`：PDF 排版程式，引用上層 `build_deck.py` 的中文字體與排字工具。
- `assets/`：本簡報的角色、辦公室、住家與生活概念圖。
- `../assets/03_city_branches.png`、`../assets/04_props_and_moods.png`：與美術設計簡報共用的城市圖、道具與圖示。`04_props_and_moods.png` 沿用舊檔名，目前是純道具與圖示板，不再含情境場景。
- `../../art/visual_style.json`：共用色名、色碼、正交投影與臺北雨天基準；不另維護一份不同色票。

封面、下班轉場與結尾共用已修訂的雨天臺北辦公室圖（`assets/09_city_office_home_cover.png`）；檔名沿用舊版，但目前圖像不是辦公室與住家的疊樓透視圖。住家另外使用 `assets/02_home_after_work.png` 展示。

PNG 以完整原圖等比例置入，未裁切或重新繪製原圖。概念圖的原始尺寸不代表正式遊戲的地圖或角色解析度。

## 重建 PDF

在專案根目錄執行：

```bash
python3 docs/presentation/sponsor/build_sponsor_deck.py \
  --content docs/presentation/sponsor/sponsor_content.json \
  --output docs/presentation/訴訟之神之路_贊助提案.pdf
```

環境需要 Python 3、`reportlab`、`fonttools`、`python-docx`，以及 Noto Sans CJK 字體。共用字體工具使用 `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` 與 `NotoSansCJK-Bold.ttc` 的繁體中文子集，將中文字體嵌入 PDF；暫存字體寫入 `/tmp/lawfirm-sponsor-fonts`。

重建只使用本專案內的來源，不需要先前的 scratch 目錄，也不會重新生成概念圖。
