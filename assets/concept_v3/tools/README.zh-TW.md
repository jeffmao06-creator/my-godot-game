# 動作素材封裝

來源必須是已生成、已確認有連續姿勢的動作圖板。工具不繪製人物、不以平移縮放代替動作，也不以資料檢查冒充美術連續性驗收。

依賴 Python 3、ImageMagick 7、FFmpeg、Pillow 及 NumPy。Pillow／NumPy 僅讀取像素做檢查；切格由 ImageMagick 無損擷取，影片由 FFmpeg 封裝。

```sh
python3 assets/concept_v3/tools/build_assets.py
python3 assets/concept_v3/tools/build_assets.py --check
```

每組圖板預設四欄三列，輸出十二張 PNG、靜態 WebP、循環 WebP、無聲 MP4，以及每幀來源矩形的 `slice_map.json`。預設前十一幀各 200 ms，末幀 600 ms，總長 2.8 秒。生成幀的手部與物件姿勢需要人工看過才可稱連續動作；自動驗證僅確認各幀像素不同、尺寸、幀數、時長及校驗碼。

`action_definitions.json` 可覆寫每組圖板的 `sheet_layout.columns`／`rows`、`margin: [left,top,right,bottom]`、`gutter: [x,y]` 與 `cell_inset: [left,top,right,bottom]`。最後一項只用於去除每格明確存在的細邊框。這些值只能依原圖實際邊界設定，工具不猜測、不補畫。尺寸無法整除時依比例向下取整定位，捨棄每格最多一個末緣像素，使幀尺寸一致。

等待其他圖板時可用 `--action write_brief --allow-missing` 先產局部檢閱版。manifest 會明列未封裝動作；最後仍需不加這些選項重建，確認十四組全部到齊。

單獨切角色等其他規則格網：

```sh
python3 assets/concept_v3/tools/cut_grid.py path/to/sheet.png --columns 6 --rows 2 --output-dir path/to/output --prefix character_
```

全部輸出都不含音樂或音效。

## 透明人物切出

```sh
python3 assets/concept_v3/tools/cut_characters.py
```

此步另需 SciPy。因部分立繪的鞋與下一排髮型越過等分線，不能直接六欄兩列切割。工具以 alpha > 4 的主要連通區辨識完整人物，將極淡邊緣按最近人物分配，再以 ImageMagick 分離鄰人及裁切，保留原人物的每個 RGBA 像素；不補畫、不重上色、不縮放。

輸出 `characters/individual/` 共 52 張透明 PNG、`character_catalog.json` 及 `exports/character_validation.json`。人物為四套主角工作／居家服、45 名員工與三名候選；不是可換裝分層系統或骨架。原始整板保留，來源邊界接觸另於驗證報告列出，人工仍需查看全身、鞋、髮及繪圖品質。
