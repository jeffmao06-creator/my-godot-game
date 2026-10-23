extends Control
## One fixed illustration per action and selected protagonist appearance.
## The modal only closes on an explicit button or Esc and never changes game data.

signal completed(action_id: String)
signal variant_changed(variant: String)

const PAPER := Color("f4efe4")
const INK := Color("17323d")
const TEAL := Color("287f7c")
const AMBER := Color("d9a648")

var _panel: PanelContainer
var _image: TextureRect
var _heading: Label
var _category: Label
var _description: Label
var _continue_button: Button
var _close: Button
var _male_button: Button
var _female_button: Button
var _action: Dictionary = {}
var _base_dir := ""
var _image_path := ""
var _action_id := ""
var _variant := "male"
var _closing := false
var _previous_focus: Control


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	visible = false
	var shade := ColorRect.new()
	shade.color = Color(0.02, 0.055, 0.065, 0.84)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	shade.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(shade)
	var centered := CenterContainer.new()
	centered.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	centered.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(centered)
	_panel = PanelContainer.new()
	_panel.custom_minimum_size = Vector2(1080, 720)
	_panel.add_theme_stylebox_override("panel", _style(PAPER, 18, 2, Color(1, 1, 1, 0.28)))
	centered.add_child(_panel)
	var content := VBoxContainer.new()
	content.add_theme_constant_override("separation", 0)
	_panel.add_child(content)
	var title_margin := MarginContainer.new()
	_margins(title_margin, 26, 18, 18, 16)
	content.add_child(title_margin)
	var title_row := HBoxContainer.new()
	title_row.add_theme_constant_override("separation", 18)
	title_margin.add_child(title_row)
	var titles := VBoxContainer.new()
	titles.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	titles.add_theme_constant_override("separation", 3)
	title_row.add_child(titles)
	_category = _label("日常", 14, TEAL)
	titles.add_child(_category)
	_heading = _label("", 28, INK)
	titles.add_child(_heading)
	var appearances := HBoxContainer.new()
	appearances.add_theme_constant_override("separation", 6)
	appearances.alignment = BoxContainer.ALIGNMENT_CENTER
	title_row.add_child(appearances)
	var group := ButtonGroup.new()
	_male_button = _appearance_button("男性主角", "male", group)
	_female_button = _appearance_button("女性主角", "female", group)
	appearances.add_child(_male_button)
	appearances.add_child(_female_button)
	_close = Button.new()
	_close.text = "×"
	_close.tooltip_text = "關閉動作圖（Esc）"
	_close.custom_minimum_size = Vector2(46, 46)
	_close.add_theme_font_size_override("font_size", 30)
	_close.add_theme_color_override("font_color", INK)
	_close.add_theme_color_override("font_hover_color", INK)
	_close.add_theme_color_override("font_focus_color", INK)
	_close.add_theme_color_override("font_pressed_color", TEAL)
	_close.add_theme_stylebox_override("normal", _style(Color(0, 0, 0, 0), 23))
	_close.add_theme_stylebox_override("hover", _style(Color("e2e6de"), 23))
	_close.add_theme_stylebox_override("focus", _style(Color(0, 0, 0, 0), 23, 2, AMBER))
	_close.pressed.connect(_finish)
	title_row.add_child(_close)
	var frame := PanelContainer.new()
	frame.custom_minimum_size = Vector2(1080, 550)
	frame.add_theme_stylebox_override("panel", _style(Color("0e242b"), 0))
	content.add_child(frame)
	_image = TextureRect.new()
	_image.custom_minimum_size = Vector2(1080, 550)
	_image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	frame.add_child(_image)
	var footer_margin := MarginContainer.new()
	_margins(footer_margin, 26, 16, 22, 18)
	content.add_child(footer_margin)
	var footer := HBoxContainer.new()
	footer.add_theme_constant_override("separation", 20)
	footer_margin.add_child(footer)
	_description = _label("", 16, Color("647979"))
	_description.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_description.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	footer.add_child(_description)
	_continue_button = Button.new()
	_continue_button.text = "繼續  →"
	_continue_button.custom_minimum_size = Vector2(140, 44)
	_continue_button.add_theme_font_size_override("font_size", 17)
	_continue_button.add_theme_color_override("font_color", PAPER)
	_continue_button.add_theme_color_override("font_hover_color", PAPER)
	_continue_button.add_theme_color_override("font_focus_color", PAPER)
	_continue_button.add_theme_color_override("font_pressed_color", PAPER)
	_continue_button.add_theme_stylebox_override("normal", _style(TEAL, 8))
	_continue_button.add_theme_stylebox_override("hover", _style(Color("359994"), 8))
	_continue_button.add_theme_stylebox_override("pressed", _style(Color("1c6361"), 8))
	_continue_button.add_theme_stylebox_override("focus", _style(Color(0, 0, 0, 0), 8, 3, AMBER))
	_continue_button.pressed.connect(_finish)
	footer.add_child(_continue_button)
	var focus_controls: Array[Control] = [_male_button, _female_button, _close, _continue_button]
	for i in focus_controls.size():
		var current: Control = focus_controls[i]
		var next: Control = focus_controls[(i + 1) % focus_controls.size()]
		var previous: Control = focus_controls[(i + focus_controls.size() - 1) % focus_controls.size()]
		current.focus_next = current.get_path_to(next)
		current.focus_previous = current.get_path_to(previous)
	set_process_unhandled_key_input(false)


func _appearance_button(title: String, variant: String, group: ButtonGroup) -> Button:
	var button := Button.new()
	button.text = title
	button.toggle_mode = true
	button.button_group = group
	button.custom_minimum_size = Vector2(104, 38)
	button.add_theme_font_size_override("font_size", 15)
	button.add_theme_color_override("font_color", INK)
	button.add_theme_color_override("font_hover_color", TEAL)
	button.add_theme_color_override("font_pressed_color", PAPER)
	button.add_theme_color_override("font_hover_pressed_color", PAPER)
	button.add_theme_stylebox_override("normal", _style(Color("e6e9df"), 7))
	button.add_theme_stylebox_override("hover", _style(Color("dce7df"), 7, 1, TEAL))
	button.add_theme_stylebox_override("pressed", _style(TEAL, 7))
	button.add_theme_stylebox_override("focus", _style(Color.TRANSPARENT, 7, 2, AMBER))
	button.pressed.connect(func(): set_variant(variant))
	return button


func show_action(action: Dictionary, base_dir: String, variant := "male") -> bool:
	if visible:
		return false
	var path := resolve_image_path(action, base_dir, variant)
	var texture := _read_texture(path) if not path.is_empty() else null
	if texture == null:
		push_error("動作插畫無法讀取: " + path)
		return false
	_action = action
	_base_dir = base_dir
	_variant = variant
	_image_path = path
	_action_id = str(action.get("id", ""))
	_heading.text = str(action.get("title", action.get("name", "日常片刻")))
	_category.text = str(action.get("category", "日常"))
	_description.text = str(action.get("description", "一個動作，一個片刻。"))
	_previous_focus = get_viewport().gui_get_focus_owner()
	_closing = false
	_image.texture = texture
	_sync_appearance_buttons()
	visible = true
	set_process_unhandled_key_input(true)
	_continue_button.grab_focus()
	return true


func set_variant(variant: String) -> bool:
	if not visible or variant not in ["male", "female"]:
		return false
	var path := resolve_image_path(_action, _base_dir, variant)
	var texture := _read_texture(path) if not path.is_empty() else null
	if texture == null:
		push_error("此角色動作插畫尚未提供: " + path)
		_sync_appearance_buttons()
		return false
	_variant = variant
	_image_path = path
	_image.texture = texture
	_sync_appearance_buttons()
	variant_changed.emit(variant)
	return true


func _sync_appearance_buttons() -> void:
	_male_button.set_pressed_no_signal(_variant == "male")
	_female_button.set_pressed_no_signal(_variant == "female")


func _finish() -> void:
	if _closing or not visible:
		return
	_closing = true
	var finished_action := _action_id
	visible = false
	set_process_unhandled_key_input(false)
	_image.texture = null
	_image_path = ""
	_action = {}
	if is_instance_valid(_previous_focus):
		_previous_focus.grab_focus()
	_closing = false
	completed.emit(finished_action)


func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		get_viewport().set_input_as_handled()
		_finish()


static func resolve_image_path(action: Dictionary, base_dir: String, variant: String) -> String:
	var images: Variant = action.get("images", {})
	if images is not Dictionary:
		return ""
	var relative := str(images.get(variant, ""))
	return base_dir.path_join(relative) if not relative.is_empty() else ""


static func _read_texture(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var loaded := load(path)
		if loaded is Texture2D:
			return loaded
	if FileAccess.file_exists(path):
		var image := Image.load_from_file(path)
		if image != null and not image.is_empty():
			return ImageTexture.create_from_image(image)
	return null


static func _label(value: String, size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = value
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	return label


static func _style(fill: Color, radius: int, border_width := 0, border := Color.TRANSPARENT) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.set_corner_radius_all(radius)
	style.set_border_width_all(border_width)
	style.border_color = border
	return style


static func _margins(container: MarginContainer, left: int, top: int, right: int, bottom: int) -> void:
	container.add_theme_constant_override("margin_left", left)
	container.add_theme_constant_override("margin_top", top)
	container.add_theme_constant_override("margin_right", right)
	container.add_theme_constant_override("margin_bottom", bottom)
