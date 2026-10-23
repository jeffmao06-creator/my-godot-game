# Godot 動作插畫展示

用 Godot 4.3 以上開啟專案根目錄的 `project.godot`，按 **F5**。選擇動作後，小視窗會顯示一張完整插畫，停留至按下「繼續」、右上角關閉或 Esc。主畫面與小視窗都能切換男性／女性主角；每位主角各有十四張動作插畫。跳槽不包含在這一版。

這是可操作的插畫展示，尚未串接疲勞、金錢、案件、時段或存檔。圖片不會逐格切換，也沒有計時、自動關閉或淡入淡出；關閉視窗不會結算遊戲資源。

上方的「事務所／回到家」切換兩張概念插畫背景，只影響展示畫面，不改變日期或時段。

## 共用素材

- 素材清單：`res://assets/concept_v3/manifest.json`（v0.4）
- 背景：`res://assets/concept_v3/environments/office.png`
- 家中背景：`res://assets/concept_v3/environments/home.png`
- 每個動作的 `images.male` 與 `images.female` 為相對素材包的完整 PNG 路徑，存放於 `action_stills/male/` 與 `action_stills/female/`。
- 僅讀取所選主角的單張插畫；缺圖會顯示錯誤，不會改讀舊影格。
- 畫面使用正常線性取樣，保留圖片比例與完整構圖。
- 中文使用系統的 Noto Sans CJK TC、微軟正黑體或蘋方字體。

## 接入正式遊戲

`action_popup.gd` 是獨立的 Control，可放入 CanvasLayer：

```gdscript
var popup = preload("res://godot_demo/action_popup.gd").new()
canvas_layer.add_child(popup)
popup.completed.connect(on_illustration_closed)
popup.show_action(action_data, "res://assets/concept_v3", "female")
```

`show_action` 回傳是否成功開窗；視窗已開啟或圖片無法讀取時回傳 `false`。`set_variant("male")`／`set_variant("female")` 可切換目前動作的主角。

`completed(action_id)` 在每次關閉時只會發送一次。`variant_changed(variant)` 在成功切換小視窗內的主角時發送。元件會保存並還原鍵盤焦點，Tab 可在主角切換、關閉及繼續按鈕之間循環；元件不自行修改遊戲資料，請由正式遊戲的主流程處理結算。

## 驗證

```sh
godot --headless --path . --editor --quit
godot --headless --path . -- --smoke-actions
```

第二個指令會逐一開啟十四個動作的男女版本，共二十八張實際圖片，確認每張停留一秒後仍為同一張圖片且視窗仍開啟，並檢查主角切換、視窗邊界、重複關閉及 Esc。所有素材產出後才可通過。
