extends Control
## Static illustrated-action showcase, with independent male and female images.

const PopupScript = preload("res://godot_demo/action_popup.gd")
const ART_DIR := "res://assets/concept_v3"
const PAPER := Color("f4efe4")
const INK := Color("17323d")
const TEAL := Color("287f7c")
const AMBER := Color("d9a648")

var _actions: Array = []
var _popup: Control
var _variant := "male"
var _male_button: Button
var _female_button: Button
var _status: Label
var _completion_count := 0
var _background: TextureRect


func _ready() -> void:
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Noto Sans CJK TC", "Microsoft JhengHei", "PingFang TC", "sans-serif"])
	var ui_theme := Theme.new()
	ui_theme.default_font = font
	ui_theme.default_font_size = 18
	theme = ui_theme
	_actions = _read_actions()
	_build_background()
	_build_content()
	var modal_layer := CanvasLayer.new()
	modal_layer.layer = 20
	add_child(modal_layer)
	_popup = PopupScript.new()
	_popup.theme = ui_theme
	modal_layer.add_child(_popup)
	_popup.completed.connect(_on_completed)
	_popup.variant_changed.connect(_on_popup_variant_changed)
	if "--smoke-actions" in OS.get_cmdline_user_args() or "--smoke-available" in OS.get_cmdline_user_args():
		call_deferred("_smoke_actions")


func _read_actions() -> Array:
	var path := ART_DIR.path_join("manifest.json")
	if not FileAccess.file_exists(path):
		return []
	var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if data is Dictionary and data.get("actions", null) is Array:
		return data["actions"]
	return []


func _build_background() -> void:
	var background := TextureRect.new()
	_background = background
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	background.texture = PopupScript._read_texture(ART_DIR.path_join("environments/office.png"))
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)
	var wash := ColorRect.new()
	wash.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	wash.color = Color(0.025, 0.075, 0.09, 0.43)
	wash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(wash)
	var gradient := Gradient.new()
	gradient.set_color(0, Color(0.035, 0.09, 0.10, 0.65))
	gradient.set_color(1, Color(0.035, 0.09, 0.10, 0.03))
	var gradient_texture := GradientTexture2D.new()
	gradient_texture.gradient = gradient
	gradient_texture.fill_from = Vector2(0, 1)
	gradient_texture.fill_to = Vector2(0, 0)
	var shading := TextureRect.new()
	shading.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	shading.texture = gradient_texture
	shading.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(shading)


func _build_content() -> void:
	var outer := MarginContainer.new()
	outer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	PopupScript._margins(outer, 52, 30, 44, 26)
	add_child(outer)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 20)
	outer.add_child(column)
	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation", 20)
	column.add_child(header)
	var identity := VBoxContainer.new()
	identity.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	identity.add_theme_constant_override("separation", 5)
	header.add_child(identity)
	identity.add_child(PopupScript._label("訴訟之神之路", 34, PAPER))
	identity.add_child(PopupScript._label("工作、生活，還有每一個選擇。", 15, Color("d4ddd5")))
	var places := HBoxContainer.new()
	places.add_theme_constant_override("separation", 6)
	places.alignment = BoxContainer.ALIGNMENT_CENTER
	header.add_child(places)
	var group := ButtonGroup.new()
	for location in [["事務所", "office.png"], ["回到家", "home.png"]]:
		var place := Button.new()
		place.text = location[0]
		place.toggle_mode = true
		place.button_group = group
		place.button_pressed = location[1] == "office.png"
		place.custom_minimum_size = Vector2(106, 42)
		place.add_theme_font_size_override("font_size", 16)
		place.add_theme_color_override("font_color", PAPER)
		place.add_theme_color_override("font_hover_color", PAPER)
		place.add_theme_color_override("font_focus_color", PAPER)
		place.add_theme_color_override("font_pressed_color", PAPER)
		place.add_theme_stylebox_override("normal", PopupScript._style(Color(0.08, 0.17, 0.19, 0.4), 8, 1, Color(1, 1, 1, 0.28)))
		place.add_theme_stylebox_override("hover", PopupScript._style(Color("3e716c"), 8))
		place.add_theme_stylebox_override("pressed", PopupScript._style(TEAL, 8))
		place.add_theme_stylebox_override("focus", PopupScript._style(Color(0, 0, 0, 0), 8, 2, AMBER))
		place.tooltip_text = "切換展示背景，不改變遊戲日期或時段。"
		var filename: String = location[1]
		place.pressed.connect(func(): _set_location(filename))
		places.add_child(place)
	var badge := Label.new()
	badge.text = "動作插畫展示"
	badge.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	badge.add_theme_font_size_override("font_size", 15)
	badge.add_theme_color_override("font_color", PAPER)
	header.add_child(badge)
	var body := HBoxContainer.new()
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation", 36)
	column.add_child(body)
	var story := VBoxContainer.new()
	story.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	story.add_theme_constant_override("separation", 16)
	body.add_child(story)
	var spacer := Control.new()
	spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
	story.add_child(spacer)
	story.add_child(PopupScript._label("每個動作，\n一張日常。", 46, PAPER))
	var synopsis := PopupScript._label("從辦公桌前的忙碌，\n到終於能安心休息的夜晚。", 22, Color("e0e6dc"))
	synopsis.add_theme_constant_override("line_spacing", 8)
	story.add_child(synopsis)
	var bottom_gap := Control.new()
	bottom_gap.custom_minimum_size.y = 18
	story.add_child(bottom_gap)
	_status = PopupScript._label("選一個動作，看看今天的片刻。", 16, Color("d2dccc"))
	_status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	story.add_child(_status)
	var card := PanelContainer.new()
	card.custom_minimum_size.x = 580
	card.add_theme_stylebox_override("panel", PopupScript._style(Color(0.956, 0.939, 0.895, 0.97), 18, 1, Color(1, 1, 1, 0.5)))
	body.add_child(card)
	var card_margin := MarginContainer.new()
	PopupScript._margins(card_margin, 26, 22, 26, 22)
	card.add_child(card_margin)
	var card_contents := VBoxContainer.new()
	card_contents.add_theme_constant_override("separation", 14)
	card_margin.add_child(card_contents)
	var card_header := HBoxContainer.new()
	card_contents.add_child(card_header)
	var card_title := PopupScript._label("今天，想做些什麼？", 24, INK)
	card_title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card_header.add_child(card_title)
	var count_label := PopupScript._label("%02d 種動作" % _actions.size(), 14, TEAL)
	count_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	card_header.add_child(count_label)
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	card_contents.add_child(scroll)
	var actions_column := VBoxContainer.new()
	actions_column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	actions_column.add_theme_constant_override("separation", 12)
	scroll.add_child(actions_column)
	var work: Array = []
	var events: Array = []
	for action in _actions:
		if str(action.get("id", "")) in ["tv_program", "news_interview", "consultation", "assign_case"]:
			events.append(action)
		else:
			work.append(action)
	_add_group(actions_column, "日常行動", work)
	_add_group(actions_column, "人物與機會", events)
	if _actions.is_empty():
		var unavailable := PopupScript._label("正在等待動作插畫。\n請先建立 concept_v3 素材包。", 18, INK)
		unavailable.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		actions_column.add_child(unavailable)
	var preferences := HBoxContainer.new()
	preferences.add_theme_constant_override("separation", 8)
	card_contents.add_child(preferences)
	var appearance_label := PopupScript._label("主角外觀", 15, Color("526d6c"))
	appearance_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	appearance_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	preferences.add_child(appearance_label)
	var appearances := ButtonGroup.new()
	_male_button = _appearance_choice("男性角色", "male", appearances)
	_female_button = _appearance_choice("女性角色", "female", appearances)
	preferences.add_child(_male_button)
	preferences.add_child(_female_button)
	_sync_appearance_buttons()
	var footer := HBoxContainer.new()
	column.add_child(footer)
	var notice := PopupScript._label("動作插畫展示・非完整遊戲流程", 13, Color("c8d3c8"))
	notice.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	footer.add_child(notice)
	footer.add_child(PopupScript._label("跳槽插畫暫不製作", 13, Color("c8d3c8")))


func _add_group(parent: VBoxContainer, title: String, actions: Array) -> void:
	if actions.is_empty():
		return
	parent.add_child(PopupScript._label(title, 14, TEAL))
	var grid := GridContainer.new()
	grid.columns = 2
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 10)
	grid.add_theme_constant_override("v_separation", 10)
	parent.add_child(grid)
	for action in actions:
		var button := Button.new()
		button.text = str(action.get("title", action.get("name", "")))
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.custom_minimum_size = Vector2(245, 52)
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.tooltip_text = str(action.get("description", ""))
		button.add_theme_font_size_override("font_size", 18)
		button.add_theme_color_override("font_color", INK)
		button.add_theme_color_override("font_hover_color", TEAL)
		button.add_theme_color_override("font_focus_color", INK)
		button.add_theme_color_override("font_pressed_color", PAPER)
		button.add_theme_color_override("font_hover_pressed_color", PAPER)
		var normal := PopupScript._style(Color(1, 1, 1, 0.72), 9, 1, Color("dae1d7"))
		normal.content_margin_left = 16
		button.add_theme_stylebox_override("normal", normal)
		var hover := PopupScript._style(Color("e0ebe3"), 9, 1, TEAL)
		hover.content_margin_left = 16
		button.add_theme_stylebox_override("hover", hover)
		var pressed := PopupScript._style(TEAL, 9)
		pressed.content_margin_left = 16
		button.add_theme_stylebox_override("pressed", pressed)
		button.add_theme_stylebox_override("focus", PopupScript._style(Color(0, 0, 0, 0), 9, 3, AMBER))
		button.pressed.connect(func(): _play_action(action))
		grid.add_child(button)


func _appearance_choice(title: String, variant: String, group: ButtonGroup) -> Button:
	var button := Button.new()
	button.text = title
	button.toggle_mode = true
	button.button_group = group
	button.custom_minimum_size = Vector2(120, 40)
	button.add_theme_font_size_override("font_size", 16)
	button.add_theme_color_override("font_color", INK)
	button.add_theme_color_override("font_hover_color", TEAL)
	button.add_theme_color_override("font_pressed_color", PAPER)
	button.add_theme_color_override("font_hover_pressed_color", PAPER)
	button.add_theme_stylebox_override("normal", PopupScript._style(Color("e3e8de"), 8))
	button.add_theme_stylebox_override("hover", PopupScript._style(Color("d8e6db"), 8, 1, TEAL))
	button.add_theme_stylebox_override("pressed", PopupScript._style(TEAL, 8))
	button.add_theme_stylebox_override("focus", PopupScript._style(Color.TRANSPARENT, 8, 2, AMBER))
	button.pressed.connect(func(): _select_variant(variant))
	return button


func _sync_appearance_buttons() -> void:
	_male_button.set_pressed_no_signal(_variant == "male")
	_female_button.set_pressed_no_signal(_variant == "female")


func _select_variant(variant: String) -> void:
	_variant = variant
	_sync_appearance_buttons()
	if is_instance_valid(_popup) and _popup.visible:
		_popup.set_variant(variant)


func _on_popup_variant_changed(variant: String) -> void:
	_variant = variant
	_sync_appearance_buttons()


func _play_action(action: Dictionary) -> void:
	var did_open: bool = _popup.show_action(action, ART_DIR, _variant)
	if not did_open:
		_status.text = "這張動作插畫尚未提供。"
	else:
		_status.text = str(action.get("title", action.get("name", ""))) + "，也是生活的一部分。"


func _set_location(filename: String) -> void:
	var texture := PopupScript._read_texture(ART_DIR.path_join("environments").path_join(filename))
	if texture != null:
		_background.texture = texture


func _on_completed(_action_id: String) -> void:
	_completion_count += 1
	_status.text = "回到自己的步調，再選下一張日常。"


func _hold_ms(milliseconds: int) -> void:
	# Verification-only wait: presentation itself has no clock, timer or animation.
	var end := Time.get_ticks_msec() + milliseconds
	while Time.get_ticks_msec() < end:
		await get_tree().process_frame


func _smoke_actions() -> void:
	# Run with godot --headless --path . -- --smoke-actions once all stills exist.
	var partial := "--smoke-available" in OS.get_cmdline_user_args()
	var tested_actions: Array = []
	for action in _actions:
		var complete := true
		for variant in ["male", "female"]:
			var path := PopupScript.resolve_image_path(action, ART_DIR, variant)
			complete = complete and not path.is_empty() and FileAccess.file_exists(path)
		if complete:
			tested_actions.append(action)
	if tested_actions.is_empty() or (not partial and tested_actions.size() != 14):
		push_error("Static smoke expected 14 complete action pairs; got %d" % tested_actions.size())
		get_tree().quit(1)
		return
	await get_tree().process_frame
	_male_button.grab_focus()
	var images_checked := 0
	for action in tested_actions:
		for variant in ["male", "female"]:
			var expected := _completion_count
			var previous_focus := get_viewport().gui_get_focus_owner()
			if not _popup.show_action(action, ART_DIR, variant):
				push_error("Cannot open static action illustration: " + str(action.get("id", "")) + "/" + variant)
				get_tree().quit(1)
				return
			await get_tree().process_frame
			var path: String = _popup._image_path
			var texture_id: int = _popup._image.texture.get_instance_id()
			if not _popup._continue_button.has_focus():
				push_error("Static modal did not receive keyboard focus")
				get_tree().quit(1)
				return
			if _popup.show_action(action, ART_DIR, variant):
				push_error("An already open illustration accepted a duplicate open")
				get_tree().quit(1)
				return
			if path != PopupScript.resolve_image_path(action, ART_DIR, variant):
				push_error("Incorrect protagonist image")
				get_tree().quit(1)
				return
			if not _popup._panel.get_global_rect().encloses(_popup._image.get_global_rect()) or _popup._image.stretch_mode != TextureRect.STRETCH_KEEP_ASPECT_CENTERED:
				push_error("Static illustration can overflow or crop its image frame")
				get_tree().quit(1)
				return
			if not get_viewport_rect().encloses(_popup._panel.get_global_rect()):
				push_error("Illustration popup extends beyond viewport")
				get_tree().quit(1)
				return
			await _hold_ms(1050)
			if not _popup.visible or _popup._image_path != path or _popup._image.texture.get_instance_id() != texture_id:
				push_error("Static illustration changed or auto-closed")
				get_tree().quit(1)
				return
			if not _popup.find_children("*", "Timer", true, false).is_empty() or not _popup.find_children("*", "AnimationPlayer", true, false).is_empty():
				push_error("Static modal has an animation clock")
				get_tree().quit(1)
				return
			_popup._finish()
			_popup._finish()
			if _popup.visible or _completion_count != expected + 1:
				push_error("Manual close was not idempotent")
				get_tree().quit(1)
				return
			if is_instance_valid(previous_focus) and not previous_focus.has_focus():
				push_error("Manual close did not restore keyboard focus")
				get_tree().quit(1)
				return
			images_checked += 1
	var action: Dictionary = tested_actions[0]
	if not _popup.show_action(action, ART_DIR, "male") or not _popup.set_variant("female"):
		get_tree().quit(1)
		return
	await _hold_ms(1050)
	if _popup._image_path != PopupScript.resolve_image_path(action, ART_DIR, "female") or not _popup.visible:
		push_error("Female appearance switch did not preserve the selected static action")
		get_tree().quit(1)
		return
	var previous := _completion_count
	var escape := InputEventKey.new()
	escape.keycode = KEY_ESCAPE
	escape.pressed = true
	Input.parse_input_event(escape)
	await get_tree().process_frame
	await get_tree().process_frame
	if _popup.visible or _completion_count != previous + 1:
		push_error("Esc did not close the static modal once")
		get_tree().quit(1)
		return
	var label := "PARTIAL" if partial else "FINAL"
	print("PASS Godot STATIC %s: %d actions, %d single images, fixed image retention, female switch, modal bounds, manual close and Esc" % [label, tested_actions.size(), images_checked])
	get_tree().quit(0)
