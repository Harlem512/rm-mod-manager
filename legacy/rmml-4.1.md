# controller
## create
```sp
-- bootstraps
if global.bootstraps == undefined {
  global.bootstraps = fun (filename) {
    let file = file_text_open_read(filename)
    let src = ""
    while !file_text_eof(file) {
      src += file_text_readln(file)
    }
    let parsed = global.__catspeak__.parseString(src)
    global.__catspeak__.compile(parsed)()
  }
}

-- rmml init
if global.rmml == undefined {
  global.bootstraps("mods/rmml/rmml_src.meow")
}

-- load mods
global.rmml.build_mod_list()
global.rmml.load_mod_list()

-- run other mod's controller_create code
let mod_cs = ds_map_find_value(global.rmml.modmap, "controller_events_create")
if mod_cs == undefined {
  return
}

-- loop over all registered events
let i = 0
while i < array_length(mod_cs) {
  -- unpack modid and code
  let elem = mod_cs[i]
  let _mod_name = elem[0]
  let _catspeak = elem[1]

  global.rmml.current_mod = _mod_name

  -- controllers and players get to speedrun their code
  _catspeak()
  i += 1
}

global.rmml.current_mod = undefined
```
## cleanup
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_cleanup",omod_controller,false,true,mn)
}
```
## step_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_step_begin",omod_controller,false,true,mn)
}
```
## step
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_step",omod_controller,false,true,mn)
}
```
## step_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_step_end",omod_controller,false,true,mn)
}
```
## draw_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_draw_begin",omod_controller,false,true,mn)
}
```
## draw
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_draw",omod_controller,false,true,mn)
}
```
## draw_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_draw_end",omod_controller,false,true,mn)
}
```
## draw_gui_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_draw_gui_begin",omod_controller,false,true,mn)
}
```
## draw_gui
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_draw_gui",omod_controller,false,true,mn)
}
```
## draw_gui_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_draw_gui_end",omod_controller,false,true,mn)
}
```
## alarm_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_alarm_0",omod_controller,false,true,mn)
}
```
## alarm_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_alarm_1",omod_controller,false,true,mn)
}
```
## alarm_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_alarm_2",omod_controller,false,true,mn)
}
```
## user_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_user_0",omod_controller,false,true,mn)
}
```
## user_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_user_1",omod_controller,false,true,mn)
}
```
## user_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_user_2",omod_controller,false,true,mn)
}
```
## room_start
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_room_start",omod_controller,false,true,mn)
}
```
## room_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_room_end",omod_controller,false,true,mn)
}
```
## destroy
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_destroy",omod_controller,false,true,mn)
}
```
## animation_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("controller_events_animation_end",omod_controller,false,true,mn)
}
```
# instance
## create
```sp
with omod_instance{
if self.mod_name != undefined { continue } global.rmml.exec("instance_events_create",omod_instance,true,false)
}
```
## cleanup
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_cleanup",omod_instance,false,false,mn)
}
```
## step_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_step_begin",omod_instance,false,false,mn)
}
```
## step
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_step",omod_instance,false,false,mn)
}
```
## step_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_step_end",omod_instance,false,false,mn)
}
```
## draw_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_draw_begin",omod_instance,false,false,mn)
}
```
## draw
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_draw",omod_instance,false,false,mn)
}
```
## draw_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_draw_end",omod_instance,false,false,mn)
}
```
## draw_gui_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_draw_gui_begin",omod_instance,false,false,mn)
}
```
## draw_gui
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_draw_gui",omod_instance,false,false,mn)
}
```
## draw_gui_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_draw_gui_end",omod_instance,false,false,mn)
}
```
## alarm_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_alarm_0",omod_instance,false,false,mn)
}
```
## alarm_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_alarm_1",omod_instance,false,false,mn)
}
```
## alarm_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_alarm_2",omod_instance,false,false,mn)
}
```
## user_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_user_0",omod_instance,false,false,mn)
}
```
## user_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_user_1",omod_instance,false,false,mn)
}
```
## user_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_user_2",omod_instance,false,false,mn)
}
```
## room_start
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_room_start",omod_instance,false,false,mn)
}
```
## room_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_room_end",omod_instance,false,false,mn)
}
```
## destroy
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_destroy",omod_instance,false,false,mn)
}
```
## animation_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("instance_events_animation_end",omod_instance,false,false,mn)
}
```
# basic
## create
```sp
with omod_basic{
if self.mod_name != undefined { continue } global.rmml.exec("basic_events_create",omod_basic,true,false)
}
```
## cleanup
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_cleanup",omod_basic,false,false,mn)
}
```
## step_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_step_begin",omod_basic,false,false,mn)
}
```
## step
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_step",omod_basic,false,false,mn)
}
```
## step_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_step_end",omod_basic,false,false,mn)
}
```
## draw_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_draw_begin",omod_basic,false,false,mn)
}
```
## draw
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_draw",omod_basic,false,false,mn)
}
```
## draw_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_draw_end",omod_basic,false,false,mn)
}
```
## draw_gui_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_draw_gui_begin",omod_basic,false,false,mn)
}
```
## draw_gui
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_draw_gui",omod_basic,false,false,mn)
}
```
## draw_gui_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_draw_gui_end",omod_basic,false,false,mn)
}
```
## alarm_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_alarm_0",omod_basic,false,false,mn)
}
```
## alarm_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_alarm_1",omod_basic,false,false,mn)
}
```
## alarm_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_alarm_2",omod_basic,false,false,mn)
}
```
## user_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_user_0",omod_basic,false,false,mn)
}
```
## user_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_user_1",omod_basic,false,false,mn)
}
```
## user_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_user_2",omod_basic,false,false,mn)
}
```
## room_start
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_room_start",omod_basic,false,false,mn)
}
```
## room_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_room_end",omod_basic,false,false,mn)
}
```
## destroy
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_destroy",omod_basic,false,false,mn)
}
```
## animation_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("basic_events_animation_end",omod_basic,false,false,mn)
}
```
# player
## create
```sp
with omod_player{
if self.mod_name != undefined { continue } global.rmml.exec("player_events_create",omod_player,true,true)
}
```
## cleanup
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_cleanup",omod_player,false,true,mn)
}
```
## step_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_step_begin",omod_player,false,true,mn)
}
```
## step
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_step",omod_player,false,true,mn)
}
```
## step_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_step_end",omod_player,false,true,mn)
}
```
## draw_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_draw_begin",omod_player,false,true,mn)
}
```
## draw
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_draw",omod_player,false,true,mn)
}
```
## draw_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_draw_end",omod_player,false,true,mn)
}
```
## draw_gui_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_draw_gui_begin",omod_player,false,true,mn)
}
```
## draw_gui
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_draw_gui",omod_player,false,true,mn)
}
```
## draw_gui_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_draw_gui_end",omod_player,false,true,mn)
}
```
## alarm_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_alarm_0",omod_player,false,true,mn)
}
```
## alarm_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_alarm_1",omod_player,false,true,mn)
}
```
## alarm_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_alarm_2",omod_player,false,true,mn)
}
```
## user_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_user_0",omod_player,false,true,mn)
}
```
## user_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_user_1",omod_player,false,true,mn)
}
```
## user_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_user_2",omod_player,false,true,mn)
}
```
## room_start
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_room_start",omod_player,false,true,mn)
}
```
## room_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_room_end",omod_player,false,true,mn)
}
```
## destroy
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_destroy",omod_player,false,true,mn)
}
```
## animation_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("player_events_animation_end",omod_player,false,true,mn)
}
```
# enemy
## create
```sp
with omod_enemy{
if self.mod_name != undefined { continue } global.rmml.exec("enemy_events_create",omod_enemy,true,false)
}
```
## cleanup
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_cleanup",omod_enemy,false,false,mn)
}
```
## step_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_step_begin",omod_enemy,false,false,mn)
}
```
## step
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_step",omod_enemy,false,false,mn)
}
```
## step_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_step_end",omod_enemy,false,false,mn)
}
```
## draw_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_draw_begin",omod_enemy,false,false,mn)
}
```
## draw
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_draw",omod_enemy,false,false,mn)
}
```
## draw_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_draw_end",omod_enemy,false,false,mn)
}
```
## draw_gui_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_draw_gui_begin",omod_enemy,false,false,mn)
}
```
## draw_gui
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_draw_gui",omod_enemy,false,false,mn)
}
```
## draw_gui_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_draw_gui_end",omod_enemy,false,false,mn)
}
```
## alarm_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_alarm_0",omod_enemy,false,false,mn)
}
```
## alarm_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_alarm_1",omod_enemy,false,false,mn)
}
```
## alarm_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_alarm_2",omod_enemy,false,false,mn)
}
```
## user_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_user_0",omod_enemy,false,false,mn)
}
```
## user_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_user_1",omod_enemy,false,false,mn)
}
```
## user_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_user_2",omod_enemy,false,false,mn)
}
```
## room_start
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_room_start",omod_enemy,false,false,mn)
}
```
## room_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_room_end",omod_enemy,false,false,mn)
}
```
## destroy
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_destroy",omod_enemy,false,false,mn)
}
```
## animation_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("enemy_events_animation_end",omod_enemy,false,false,mn)
}
```
# hitbox
## create
```sp
with omod_hitbox{
if self.mod_name != undefined { continue } global.rmml.exec("hitbox_events_create",omod_hitbox,true,false)
}
```
## cleanup
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_cleanup",omod_hitbox,false,false,mn)
}
```
## step_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_step_begin",omod_hitbox,false,false,mn)
}
```
## step
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_step",omod_hitbox,false,false,mn)
}
```
## step_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_step_end",omod_hitbox,false,false,mn)
}
```
## draw_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_draw_begin",omod_hitbox,false,false,mn)
}
```
## draw
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_draw",omod_hitbox,false,false,mn)
}
```
## draw_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_draw_end",omod_hitbox,false,false,mn)
}
```
## draw_gui_begin
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_draw_gui_begin",omod_hitbox,false,false,mn)
}
```
## draw_gui
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_draw_gui",omod_hitbox,false,false,mn)
}
```
## draw_gui_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_draw_gui_end",omod_hitbox,false,false,mn)
}
```
## alarm_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_alarm_0",omod_hitbox,false,false,mn)
}
```
## alarm_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_alarm_1",omod_hitbox,false,false,mn)
}
```
## alarm_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_alarm_2",omod_hitbox,false,false,mn)
}
```
## user_0
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_user_0",omod_hitbox,false,false,mn)
}
```
## user_1
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_user_1",omod_hitbox,false,false,mn)
}
```
## user_2
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_user_2",omod_hitbox,false,false,mn)
}
```
## room_start
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_room_start",omod_hitbox,false,false,mn)
}
```
## room_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_room_end",omod_hitbox,false,false,mn)
}
```
## destroy
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_destroy",omod_hitbox,false,false,mn)
}
```
## animation_end
```sp
let mn=self.mod_name
with self {
global.rmml.exec("hitbox_events_animation_end",omod_hitbox,false,false,mn)
}
```