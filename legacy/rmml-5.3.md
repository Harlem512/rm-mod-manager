# controller
## create
```sp
-- bootstraps
if global.bootstraps == undefined {
  global.bootstraps = fun (filename) {
    let buff = buffer_load(filename)
    let parsed = global.__catspeak__.parse(buff)
    buffer_delete(buff)
    global.__catspeak__.compile(parsed)
  }
}

-- rmml init
if global.rmml == undefined {
  global.bootstraps("mods/rmml/rmml_src.meow")()
}

-- load mods
global.rmml.__build_mod_list()
global.rmml.__load_mod_list()

-- run other mod's controller_create code
with self {
  global.rmml.exec("controller_events_create",true,true)
}

-- purge the modmap
if global.rmml.purge {
  global.rmml.purge_fn()
}
```
## cleanup
```sp
with self {global.rmml.exec("controller_events_cleanup",false,true)
}
```
## step_begin
```sp
with self {global.rmml.exec("controller_events_step_begin",false,true)
}
```
## step
```sp
with self {global.rmml.exec("controller_events_step",false,true)
}
```
## step_end
```sp
with self {global.rmml.exec("controller_events_step_end",false,true)
}
```
## draw_begin
```sp
with self {global.rmml.exec("controller_events_draw_begin",false,true)
}
```
## draw
```sp
with self {global.rmml.exec("controller_events_draw",false,true)
}
```
## draw_end
```sp
with self {global.rmml.exec("controller_events_draw_end",false,true)
}
```
## draw_gui_begin
```sp
with self {global.rmml.exec("controller_events_draw_gui_begin",false,true)
}
```
## draw_gui
```sp
with self {global.rmml.exec("controller_events_draw_gui",false,true)
}
```
## draw_gui_end
```sp
with self {global.rmml.exec("controller_events_draw_gui_end",false,true)
}
```
## alarm_0
```sp
with self {global.rmml.exec("controller_events_alarm_0",false,true)
}
```
## alarm_1
```sp
with self {global.rmml.exec("controller_events_alarm_1",false,true)
}
```
## alarm_2
```sp
with self {global.rmml.exec("controller_events_alarm_2",false,true)
}
```
## user_0
```sp
with self {global.rmml.exec("controller_events_user_0",false,true)
}
```
## user_1
```sp
with self {global.rmml.exec("controller_events_user_1",false,true)
}
```
## user_2
```sp
with self {global.rmml.exec("controller_events_user_2",false,true)
}
```
## room_start
```sp
with self {global.rmml.exec("controller_events_room_start",false,true)
}
```
## room_end
```sp
with self {global.rmml.exec("controller_events_room_end",false,true)
}
```
## destroy
```sp
with self {global.rmml.exec("controller_events_destroy",false,true)
}
```
## animation_end
```sp
with self {global.rmml.exec("controller_events_animation_end",false,true)
}
```
# instance
## create
```sp
with omod_instance {if self.mod_name != undefined { continue } self.mod_name=global.rmml.current_mod
global.rmml.exec("instance_events_create",true,false)
}
```
## cleanup
```sp
with self {global.rmml.exec("instance_events_cleanup",false,false)
}
```
## step_begin
```sp
with self {global.rmml.exec("instance_events_step_begin",false,false)
}
```
## step
```sp
with self {global.rmml.exec("instance_events_step",false,false)
}
```
## step_end
```sp
with self {global.rmml.exec("instance_events_step_end",false,false)
}
```
## draw_begin
```sp
with self {global.rmml.exec("instance_events_draw_begin",false,false)
}
```
## draw
```sp
with self {global.rmml.exec("instance_events_draw",false,false)
}
```
## draw_end
```sp
with self {global.rmml.exec("instance_events_draw_end",false,false)
}
```
## draw_gui_begin
```sp
with self {global.rmml.exec("instance_events_draw_gui_begin",false,false)
}
```
## draw_gui
```sp
with self {global.rmml.exec("instance_events_draw_gui",false,false)
}
```
## draw_gui_end
```sp
with self {global.rmml.exec("instance_events_draw_gui_end",false,false)
}
```
## alarm_0
```sp
with self {global.rmml.exec("instance_events_alarm_0",false,false)
}
```
## alarm_1
```sp
with self {global.rmml.exec("instance_events_alarm_1",false,false)
}
```
## alarm_2
```sp
with self {global.rmml.exec("instance_events_alarm_2",false,false)
}
```
## user_0
```sp
with self {global.rmml.exec("instance_events_user_0",false,false)
}
```
## user_1
```sp
with self {global.rmml.exec("instance_events_user_1",false,false)
}
```
## user_2
```sp
with self {global.rmml.exec("instance_events_user_2",false,false)
}
```
## room_start
```sp
with self {global.rmml.exec("instance_events_room_start",false,false)
}
```
## room_end
```sp
with self {global.rmml.exec("instance_events_room_end",false,false)
}
```
## destroy
```sp
with self {global.rmml.exec("instance_events_destroy",false,false)
}
```
## animation_end
```sp
with self {global.rmml.exec("instance_events_animation_end",false,false)
}
```
# basic
## create
```sp
with omod_basic {if self.mod_name != undefined { continue } self.mod_name=global.rmml.current_mod
global.rmml.exec("basic_events_create",true,false)
}
```
## cleanup
```sp
with self {global.rmml.exec("basic_events_cleanup",false,false)
}
```
## step_begin
```sp
with self {global.rmml.exec("basic_events_step_begin",false,false)
}
```
## step
```sp
with self {global.rmml.exec("basic_events_step",false,false)
}
```
## step_end
```sp
with self {global.rmml.exec("basic_events_step_end",false,false)
}
```
## draw_begin
```sp
with self {global.rmml.exec("basic_events_draw_begin",false,false)
}
```
## draw
```sp
with self {global.rmml.exec("basic_events_draw",false,false)
}
```
## draw_end
```sp
with self {global.rmml.exec("basic_events_draw_end",false,false)
}
```
## draw_gui_begin
```sp
with self {global.rmml.exec("basic_events_draw_gui_begin",false,false)
}
```
## draw_gui
```sp
with self {global.rmml.exec("basic_events_draw_gui",false,false)
}
```
## draw_gui_end
```sp
with self {global.rmml.exec("basic_events_draw_gui_end",false,false)
}
```
## alarm_0
```sp
with self {global.rmml.exec("basic_events_alarm_0",false,false)
}
```
## alarm_1
```sp
with self {global.rmml.exec("basic_events_alarm_1",false,false)
}
```
## alarm_2
```sp
with self {global.rmml.exec("basic_events_alarm_2",false,false)
}
```
## user_0
```sp
with self {global.rmml.exec("basic_events_user_0",false,false)
}
```
## user_1
```sp
with self {global.rmml.exec("basic_events_user_1",false,false)
}
```
## user_2
```sp
with self {global.rmml.exec("basic_events_user_2",false,false)
}
```
## room_start
```sp
with self {global.rmml.exec("basic_events_room_start",false,false)
}
```
## room_end
```sp
with self {global.rmml.exec("basic_events_room_end",false,false)
}
```
## destroy
```sp
with self {global.rmml.exec("basic_events_destroy",false,false)
}
```
## animation_end
```sp
with self {global.rmml.exec("basic_events_animation_end",false,false)
}
```
# player
## create
```sp
with omod_player {if self.mod_name != undefined { continue } self.mod_name=global.rmml.current_mod
global.rmml.exec("player_events_create",true,false)
}
```
## cleanup
```sp
with omod_player {global.rmml.exec("player_events_cleanup",false,false)
}
```
## step_begin
```sp
with omod_player {global.rmml.exec("player_events_step_begin",false,false)
}
```
## step
```sp
with omod_player {global.rmml.exec("player_events_step",false,false)
}
```
## step_end
```sp
with omod_player {global.rmml.exec("player_events_step_end",false,false)
}
```
## draw_begin
```sp
with omod_player {global.rmml.exec("player_events_draw_begin",false,false)
}
```
## draw
```sp
with omod_player {global.rmml.exec("player_events_draw",false,false)
}
```
## draw_end
```sp
with omod_player {global.rmml.exec("player_events_draw_end",false,false)
}
```
## draw_gui_begin
```sp
with omod_player {global.rmml.exec("player_events_draw_gui_begin",false,false)
}
```
## draw_gui
```sp
with omod_player {global.rmml.exec("player_events_draw_gui",false,false)
}
```
## draw_gui_end
```sp
with omod_player {global.rmml.exec("player_events_draw_gui_end",false,false)
}
```
## alarm_0
```sp
with omod_player {global.rmml.exec("player_events_alarm_0",false,false)
}
```
## alarm_1
```sp
with omod_player {global.rmml.exec("player_events_alarm_1",false,false)
}
```
## alarm_2
```sp
with omod_player {global.rmml.exec("player_events_alarm_2",false,false)
}
```
## user_0
```sp
with omod_player {global.rmml.exec("player_events_user_0",false,false)
}
```
## user_1
```sp
with omod_player {global.rmml.exec("player_events_user_1",false,false)
}
```
## user_2
```sp
with omod_player {global.rmml.exec("player_events_user_2",false,false)
}
```
## room_start
```sp
with omod_player {global.rmml.exec("player_events_room_start",false,false)
}
```
## room_end
```sp
with omod_player {global.rmml.exec("player_events_room_end",false,false)
}
```
## destroy
```sp
with omod_player {global.rmml.exec("player_events_destroy",false,false)
}
```
## animation_end
```sp
with omod_player {global.rmml.exec("player_events_animation_end",false,false)
}
```
# enemy
## create
```sp
with omod_enemy {if self.mod_name != undefined { continue } self.mod_name=global.rmml.current_mod
global.rmml.exec("enemy_events_create",true,false)
}
```
## cleanup
```sp
with self {global.rmml.exec("enemy_events_cleanup",false,false)
}
```
## step_begin
```sp
with self {global.rmml.exec("enemy_events_step_begin",false,false)
}
```
## step
```sp
with self {global.rmml.exec("enemy_events_step",false,false)
}
```
## step_end
```sp
with self {global.rmml.exec("enemy_events_step_end",false,false)
}
```
## draw_begin
```sp
with self {global.rmml.exec("enemy_events_draw_begin",false,false)
}
```
## draw
```sp
with self {global.rmml.exec("enemy_events_draw",false,false)
}
```
## draw_end
```sp
with self {global.rmml.exec("enemy_events_draw_end",false,false)
}
```
## draw_gui_begin
```sp
with self {global.rmml.exec("enemy_events_draw_gui_begin",false,false)
}
```
## draw_gui
```sp
with self {global.rmml.exec("enemy_events_draw_gui",false,false)
}
```
## draw_gui_end
```sp
with self {global.rmml.exec("enemy_events_draw_gui_end",false,false)
}
```
## alarm_0
```sp
with self {global.rmml.exec("enemy_events_alarm_0",false,false)
}
```
## alarm_1
```sp
with self {global.rmml.exec("enemy_events_alarm_1",false,false)
}
```
## alarm_2
```sp
with self {global.rmml.exec("enemy_events_alarm_2",false,false)
}
```
## user_0
```sp
with self {global.rmml.exec("enemy_events_user_0",false,false)
}
```
## user_1
```sp
with self {global.rmml.exec("enemy_events_user_1",false,false)
}
```
## user_2
```sp
with self {global.rmml.exec("enemy_events_user_2",false,false)
}
```
## room_start
```sp
with self {global.rmml.exec("enemy_events_room_start",false,false)
}
```
## room_end
```sp
with self {global.rmml.exec("enemy_events_room_end",false,false)
}
```
## destroy
```sp
with self {global.rmml.exec("enemy_events_destroy",false,false)
}
```
## animation_end
```sp
with self {global.rmml.exec("enemy_events_animation_end",false,false)
}
```
# hitbox
## create
```sp
with omod_hitbox {if self.mod_name != undefined { continue } self.mod_name=global.rmml.current_mod
global.rmml.exec("hitbox_events_create",true,false)
}
```
## cleanup
```sp
with self {global.rmml.exec("hitbox_events_cleanup",false,false)
}
```
## step_begin
```sp
with self {global.rmml.exec("hitbox_events_step_begin",false,false)
}
```
## step
```sp
with self {global.rmml.exec("hitbox_events_step",false,false)
}
```
## step_end
```sp
with self {global.rmml.exec("hitbox_events_step_end",false,false)
}
```
## draw_begin
```sp
with self {global.rmml.exec("hitbox_events_draw_begin",false,false)
}
```
## draw
```sp
with self {global.rmml.exec("hitbox_events_draw",false,false)
}
```
## draw_end
```sp
with self {global.rmml.exec("hitbox_events_draw_end",false,false)
}
```
## draw_gui_begin
```sp
with self {global.rmml.exec("hitbox_events_draw_gui_begin",false,false)
}
```
## draw_gui
```sp
with self {global.rmml.exec("hitbox_events_draw_gui",false,false)
}
```
## draw_gui_end
```sp
with self {global.rmml.exec("hitbox_events_draw_gui_end",false,false)
}
```
## alarm_0
```sp
with self {global.rmml.exec("hitbox_events_alarm_0",false,false)
}
```
## alarm_1
```sp
with self {global.rmml.exec("hitbox_events_alarm_1",false,false)
}
```
## alarm_2
```sp
with self {global.rmml.exec("hitbox_events_alarm_2",false,false)
}
```
## user_0
```sp
with self {global.rmml.exec("hitbox_events_user_0",false,false)
}
```
## user_1
```sp
with self {global.rmml.exec("hitbox_events_user_1",false,false)
}
```
## user_2
```sp
with self {global.rmml.exec("hitbox_events_user_2",false,false)
}
```
## room_start
```sp
with self {global.rmml.exec("hitbox_events_room_start",false,false)
}
```
## room_end
```sp
with self {global.rmml.exec("hitbox_events_room_end",false,false)
}
```
## destroy
```sp
with self {global.rmml.exec("hitbox_events_destroy",false,false)
}
```
## animation_end
```sp
with self {global.rmml.exec("hitbox_events_animation_end",false,false)
}
```