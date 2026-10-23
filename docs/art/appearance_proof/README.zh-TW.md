# 48 人分層外觀結構驗證原型

這是一個可離線開啟的 SVG 組裝介面，用來檢查 45 名員工與 3 名招募候選的結構差異、圖層順序，以及同一外觀資料組裝肖像與全身的一致性。**它不是最終遊戲像素美術，也不代表動畫素材已完成。**

- 開啟 `index.html`：9 × 5 員工名單與 3 人招募列。點擊人物可查看固定保存的外觀資料，並逐層切換可見性。
- 開啟 `index.html?view=layers`：同一角色的分層組裝示意。
- `48_roster_proof.png`：1920 × 1080 的名單驗證畫面。
- `48_roster_wide.png`：2400 × 840 的簡報用 12 × 4 名單；末三格以綠框標示招募候選。
- `portrait_layers_proof.png`：1600 × 900 的分層驗證畫面。
- `proof_validation.json`：實際名單、結構覆蓋、來源雜湊與瀏覽器檢查結果。

唯一的身份來源為上層 `appearance_manifest.json`。渲染時不抽籤；重開、重繪或關閉圖層都不改寫角色身份。顏色不計入結構去重，48 人的「臉型＋髮型」及「身形＋髮型」配對均不重複。圖示以直線、階梯輪廓及 SVG 圖層製作，沒有切割或改圖既有概念圖。

由專案根目錄重新建立：

```sh
python3 docs/art/appearance_proof/build_appearance_proof.py
python3 docs/art/appearance_proof/render_appearance_proof.py
```

後者需要 Python Playwright 與 `/usr/bin/chromium`。正式遊戲製作仍需校正各身形與動作的衣著、髮型、配件、遮擋、腳底錨點及像素密度。
