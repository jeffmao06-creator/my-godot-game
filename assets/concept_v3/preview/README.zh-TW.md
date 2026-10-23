# 訴訟之神之路｜動作插畫素材檢視

每個動作由一張完整插畫呈現，提供男性與女性主角版本；14 種動作共 28 張 PNG，跳槽不包含在內。點圖開啟小視窗後，圖片會一直保留，直到手動選擇「繼續」、關閉或按 Esc。沒有自動播放、重播、秒數、進度或圖片切換動畫。

頁面另保留 52 張人物立繪（4 張主角外觀、45 位員工、3 位招募候選）與辦公室、下班後住家兩個場景。

## 開啟方式

完整下載專案後，直接用瀏覽器開啟本資料夾的 [index.html](index.html)。素材清單已嵌入離線資料，不需要外部網站、字型或服務。

也可以在專案根目錄執行：

~~~sh
python3 -m http.server 8000
~~~

再開啟 http://localhost:8000/assets/concept_v3/preview/index.html 。

網址可加上 ?gender=female 先選女性主角；?action=research 只選取「查找資料」而不自動開窗。?view=characters 與 ?view=environments 直接切換至人物與場景素材。

## 更新清單與驗證

清單中的每個動作必須同時提供 images.male 與 images.female，路徑相對於 concept_v3 資料夾。靜態動作不回退讀取舊逐格素材。

更新 manifest.json 或人物清單後，從專案根目錄執行：

~~~sh
python3 assets/concept_v3/preview/build_preview.py
python3 assets/concept_v3/preview/validate_preview.py
~~~

驗證會逐一開啟男女共 28 張全尺寸圖片，確認每張超過一秒仍顯示相同 PNG、手動繼續與 Esc 關閉、切換男女保留同一動作、鍵盤焦點返回、52 張人物與兩個場景完整載入，以及手機版圖片不超出視窗。驗證結果與截圖放在 qa；validation.json 同時記錄實際驗證時的來源 SHA-256。

此頁是靜態素材展示。圖片檢視與主角外觀切換不結算遊戲時間、疲勞或金錢；遊戲主流程另處理資源與選項結果。Godot 入口請參考 [project.godot](../../../project.godot) 與 [Godot 展示說明](../../../godot_demo/README.zh-TW.md)。
