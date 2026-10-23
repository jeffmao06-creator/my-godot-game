extends Control
## A self-contained modal that plays the supplied drawings, one frame at a time.
## It never changes game time, resources, cases or the source manifest.

signal completed(action_id: String, skipped: bool)

const PAPER := Color("f4efe4")
const INK := Color("17323d")
const TEAL := Color("287f7c")
const AMBER := Color("d9a648")

var _panel: PanelContainer
var _image: TextureRect
var _heading: Label
var _category: Label
var _skip: Button
var _close: Button
var _progress: ProgressBar
var _timer: Timer
var _textures: Array[Texture2D] = []
var _durations: Array[float] = []
var _frame_index := 0
var _elapsed := 0.0
var _total := 0.0
var _action_id := ""
var _running := false
var _finishing := false
var _static_preview := false
var _previous_focus: Control
var _tween: Tween


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
	_panel.custom_minimum_size = Vector2(1060, 690)
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
	_close = Button.new()
	_close.text = "×"
	_close.tooltip_text = "關閉過場（Esc）"
	_close.custom_minimum_size = Vector2(46, 46)
	_close.add_theme_font_size_override("font_size", 30)
	_close.add_theme_color_override("font_color", INK)
	_close.add_theme_color_override("font_hover_color", INK)
	_close.add_theme_color_override("font_focus_color", INK)
	_close.add_theme_color_override("font_pressed_color", TEAL)
	_close.add_theme_stylebox_override("normal", _style(Color(0, 0, 0, 0), 23))
	_close.add_theme_stylebox_override("hover", _style(Color("e2e6de"), 23))
	_close.add_theme_stylebox_override("focus", _style(Color(0, 0, 0, 0), 23, 2, AMBER))
	_close.pressed.connect(func(): _finish(true))
	title_row.add_child(_close)
	var frame := PanelContainer.new()
	frame.custom_minimum_size = Vector2(1060, 500)
	frame.add_theme_stylebox_override("panel", _style(Color("0e242b"), 0))
	content.add_child(frame)
	_image = TextureRect.new()
	_image.custom_minimum_size = Vector2(1060, 500)
	_image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	frame.add_child(_image)
	_progress = ProgressBar.new()
	_progress.custom_minimum_size.y = 4
	_progress.show_percentage = false
	_progress.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_progress.add_theme_stylebox_override("background", _style(Color("d8dfd6"), 0))
	_progress.add_theme_stylebox_override("fill", _style(TEAL, 0))
	content.add_child(_progress)
	var footer_margin := MarginContainer.new()
	_margins(footer_margin, 26, 16, 22, 18)
	content.add_child(footer_margin)
	var footer := HBoxContainer.new()
	footer_margin.add_child(footer)
	var hint := _label("一段日常，一個片刻。", 16, Color("647979"))
	hint.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	footer.add_child(hint)
	_skip = Button.new()
	_skip.text = "略過  →"
	_skip.custom_minimum_size = Vector2(140, 44)
	_skip.add_theme_font_size_override("font_size", 17)
	_skip.add_theme_color_override("font_color", PAPER)
	_skip.add_theme_color_override("font_hover_color", PAPER)
	_skip.add_theme_color_override("font_focus_color", PAPER)
	_skip.add_theme_color_override("font_pressed_color", PAPER)
	_skip.add_theme_stylebox_override("normal", _style(TEAL, 8))
	_skip.add_theme_stylebox_override("hover", _style(Color("359994"), 8))
	_skip.add_theme_stylebox_override("pressed", _style(Color("1c6361"), 8))
	_skip.add_theme_stylebox_override("focus", _style(Color(0, 0, 0, 0), 8, 3, AMBER))
	_skip.pressed.connect(func(): _finish(true))
	footer.add_child(_skip)
	_close.focus_next = _close.get_path_to(_skip)
	_close.focus_previous = _close.get_path_to(_skip)
	_skip.focus_next = _skip.get_path_to(_close)
	_skip.focus_previous = _skip.get_path_to(_close)
	_close.focus_neighbor_left = _close.get_path_to(_skip)
	_close.focus_neighbor_right = _close.get_path_to(_skip)
	_close.focus_neighbor_top = _close.get_path_to(_skip)
	_close.focus_neighbor_bottom = _close.get_path_to(_skip)
	_skip.focus_neighbor_left = _skip.get_path_to(_close)
	_skip.focus_neighbor_right = _skip.get_path_to(_close)
	_skip.focus_neighbor_top = _skip.get_path_to(_close)
	_skip.focus_neighbor_bottom = _skip.get_path_to(_close)
	_timer = Timer.new()
	_timer.one_shot = true
	_timer.timeout.connect(_advance)
	add_child(_timer)
	set_process(false)
	set_process_unhandled_key_input(false)


func play(action: Dictionary, base_dir: String, static_preview := false) -> bool:
	if visible:
		return false
	_textures.clear()
	_durations.clear()
	var frames: Array = action.get("frames", [])
	var times: Array = action.get("frame_durations_ms", [])
	for i in frames.size():
		var frame: Variant = frames[i]
		var relative: String = str(frame.get("src", "")) if frame is Dictionary else str(frame)
		var texture := _read_texture(base_dir.path_join(relative))
		if texture == null:
			push_error("過場影格無法讀取: " + relative)
			_textures.clear()
			return false
		_textures.append(texture)
		var ms := float(times[i]) if i < times.size() else 200.0
		if frame is Dictionary:
			ms = float(frame.get("duration_ms", ms))
		_durations.append(maxf(ms / 1000.0, 0.016))
	if _textures.is_empty():
		return false
	_action_id = str(action.get("id", ""))
	_heading.text = str(action.get("title", action.get("name", "日常片刻")))
	_category.text = str(action.get("category", "日常"))
	_previous_focus = get_viewport().gui_get_focus_owner()
	_frame_index = 0
	_elapsed = 0.0
	_total = 0.0
	for duration in _durations:
		_total += duration
	_finishing = false
	_static_preview = static_preview
	_running = not static_preview
	_progress.value = 0
	_image.texture = _textures[0]
	_skip.text = "關閉  →" if static_preview else "略過  →"
	visible = true
	modulate.a = 1.0 if static_preview else 0.0
	set_process(_running)
	set_process_unhandled_key_input(true)
	_skip.grab_focus()
	if is_instance_valid(_tween):
		_tween.kill()
	if not static_preview:
		_tween = create_tween()
		_tween.tween_property(self, "modulate:a", 1.0, 0.16)
		_timer.start(_durations[0])
	return true


func _process(delta: float) -> void:
	if not _running:
		return
	_elapsed += delta
	_progress.value = minf(100.0, (_elapsed / _total) * 100.0)


func _advance() -> void:
	if not _running or _finishing:
		return
	_frame_index += 1
	if _frame_index >= _textures.size():
		_progress.value = 100
		_finish(false)
		return
	_image.texture = _textures[_frame_index]
	_timer.start(_durations[_frame_index])


func _finish(skipped: bool) -> void:
	if _finishing or not visible:
		return
	_finishing = true
	_running = false
	_timer.stop()
	set_process(false)
	set_process_unhandled_key_input(false)
	if is_instance_valid(_tween):
		_tween.kill()
	if not _static_preview:
		_tween = create_tween()
		_tween.tween_property(self, "modulate:a", 0.0, 0.14)
		await _tween.finished
	visible = false
	_image.texture = null
	_textures.clear()
	if is_instance_valid(_previous_focus):
		_previous_focus.grab_focus()
	completed.emit(_action_id, skipped)


func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		get_viewport().set_input_as_handled()
		_finish(true)


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
