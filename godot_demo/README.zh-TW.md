# Godot 動作過場展示

用 Godot 4.3 以上開啟專案根目錄的 `project.godot`，按 **F5**。選擇一個動作，就會在小視窗逐格播放同一份素材包的實際繪製影格；播放完成後關閉，亦可按「略過」、右上角關閉或 Esc。跳槽不包含在這一版。

這是可操作的動畫展示，尚未串接疲勞、金錢、案件、時段或存檔。播放及略過都不會結算遊戲資源。靜態預覽開關可停用畫面播放與淡入淡出。

上方的「事務所／回到家」切換兩張概念插畫背景，只影響展示畫面，不改變日期或時段。

## 共用素材

- 素材與動畫清單：`res://assets/concept_v3/manifest.json`
- 背景：`res://assets/concept_v3/environments/office.png`
- 每個動作的 `frames` 為相對素材包的 PNG 路徑；`frame_durations_ms` 與其等長。
- 畫面使用正常線性取樣，不強制縮為像素精靈，也不以整圖平移、縮放冒充動作。
- 中文使用系統的 Noto Sans CJK TC、微軟正黑體或蘋方字體。

## 接入正式遊戲

`action_popup.gd` 是獨立的 Control，可放入 CanvasLayer：

```gdscript
var popup = preload("res://godot_demo/action_popup.gd").new()
canvas_layer.add_child(popup)
popup.completed.connect(on_cutscene_completed)
popup.play(action_data, "res://assets/concept_v3", false)
```

`completed(action_id, skipped)` 每次只會發送一次，供正式遊戲在自己的流程內處理結算；元件不自行修改資料。請由主流程避免重複呼叫動作結算。

## 驗證

```sh
godot --headless --path . --editor --quit
godot --headless --path . -- --smoke-actions
```

第二個指令會以實際素材連續播放十四個動作，再檢查重複關閉、略過與靜態預覽；所有素材產出後才可通過。
