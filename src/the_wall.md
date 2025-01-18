
# controller
## create
```
global.thewall={}
global.thewall["controller_create"]=self.depth
```
## room_start
```
global.object_types = [
    omod_player,
    omod_instance,
    omod_basic,
    omod_enemy,
    omod_hitbox,
]

if instance_number(omenu_new) != 0 {
    with omenu_new {
        self.state = 8
        self.menu_select = 0
        self.start_timer = 100
    }
    return
}

let i = 0
while (i < array_length(global.object_types)) {
    let t = global.object_types[i]
    i += 1

    let inst = instance_create_depth(0, 10 * i, -50 * i, t)
}
```
# controller
## cleanup
```
global.thewall["controller_cleanup"]=self.depth
```
## step_begin
```
global.thewall["controller_step_begin"]=self.depth
```
## step
```
global.thewall["controller_step"]=self.depth
```
## step_end
```
global.thewall["controller_step_end"]=self.depth
```
## draw_begin
```
global.thewall["controller_draw_begin"]=self.depth
```
## draw
```
global.thewall["controller_draw"]=self.depth
```
## draw_end
```
global.thewall["controller_draw_end"]=self.depth
```
## draw_gui_begin
```
global.thewall["controller_draw_gui_begin"]=self.depth
```
## draw_gui
```
global.thewall["controller_draw_gui"]=self.depth
```
## draw_gui_end
```
global.thewall["controller_draw_gui_end"]=self.depth
```
## alarm_0
```
global.thewall["controller_alarm_0"]=self.depth
```
## alarm_1
```
global.thewall["controller_alarm_1"]=self.depth
```
## alarm_2
```
global.thewall["controller_alarm_2"]=self.depth
```
## user_0
```
global.thewall["controller_user_0"]=self.depth
```
## user_1
```
global.thewall["controller_user_1"]=self.depth
```
## user_2
```
global.thewall["controller_user_2"]=self.depth
```
## room_start
```
global.thewall["controller_room_start"]=self.depth
```
## room_end
```
global.thewall["controller_room_end"]=self.depth
```
## destroy
```
global.thewall["controller_destroy"]=self.depth
```
## animation_end
```
global.thewall["controller_animation_end"]=self.depth
```
# instance
## create
```
global.thewall["instance_create"]=self.depth
```
## cleanup
```
global.thewall["instance_cleanup"]=self.depth
```
## step_begin
```
global.thewall["instance_step_begin"]=self.depth
```
## step
```
global.thewall["instance_step"]=self.depth
```
## step_end
```
global.thewall["instance_step_end"]=self.depth
```
## draw_begin
```
global.thewall["instance_draw_begin"]=self.depth
```
## draw
```
global.thewall["instance_draw"]=self.depth
```
## draw_end
```
global.thewall["instance_draw_end"]=self.depth
```
## draw_gui_begin
```
global.thewall["instance_draw_gui_begin"]=self.depth
```
## draw_gui
```
global.thewall["instance_draw_gui"]=self.depth
```
## draw_gui_end
```
global.thewall["instance_draw_gui_end"]=self.depth
```
## alarm_0
```
global.thewall["instance_alarm_0"]=self.depth
```
## alarm_1
```
global.thewall["instance_alarm_1"]=self.depth
```
## alarm_2
```
global.thewall["instance_alarm_2"]=self.depth
```
## user_0
```
global.thewall["instance_user_0"]=self.depth
```
## user_1
```
global.thewall["instance_user_1"]=self.depth
```
## user_2
```
global.thewall["instance_user_2"]=self.depth
```
## room_start
```
global.thewall["instance_room_start"]=self.depth
```
## room_end
```
global.thewall["instance_room_end"]=self.depth
```
## destroy
```
global.thewall["instance_destroy"]=self.depth
```
## animation_end
```
global.thewall["instance_animation_end"]=self.depth
```
# basic
## create
```
global.thewall["basic_create"]=self.depth
```
## cleanup
```
global.thewall["basic_cleanup"]=self.depth
```
## step_begin
```
global.thewall["basic_step_begin"]=self.depth
```
## step
```
global.thewall["basic_step"]=self.depth
```
## step_end
```
global.thewall["basic_step_end"]=self.depth
```
## draw_begin
```
global.thewall["basic_draw_begin"]=self.depth
```
## draw
```
global.thewall["basic_draw"]=self.depth
```
## draw_end
```
global.thewall["basic_draw_end"]=self.depth
```
## draw_gui_begin
```
global.thewall["basic_draw_gui_begin"]=self.depth
```
## draw_gui
```
global.thewall["basic_draw_gui"]=self.depth
```
## draw_gui_end
```
global.thewall["basic_draw_gui_end"]=self.depth
```
## alarm_0
```
global.thewall["basic_alarm_0"]=self.depth
```
## alarm_1
```
global.thewall["basic_alarm_1"]=self.depth
```
## alarm_2
```
global.thewall["basic_alarm_2"]=self.depth
```
## user_0
```
global.thewall["basic_user_0"]=self.depth
```
## user_1
```
global.thewall["basic_user_1"]=self.depth
```
## user_2
```
global.thewall["basic_user_2"]=self.depth
```
## room_start
```
global.thewall["basic_room_start"]=self.depth
```
## room_end
```
global.thewall["basic_room_end"]=self.depth
```
## destroy
```
global.thewall["basic_destroy"]=self.depth
```
## animation_end
```
global.thewall["basic_animation_end"]=self.depth
```
# player
## create
```
event_inherited()
global.thewall["player_create"]=self.depth
```
## cleanup
```
event_inherited()
global.thewall["player_cleanup"]=self.depth
```
## step_begin
```
event_inherited()
global.thewall["player_step_begin"]=self.depth
```
## step
```
event_inherited()
global.thewall["player_step"]=self.depth
```
## step_end
```
event_inherited()
global.thewall["player_step_end"]=self.depth
```
## draw_begin
```
event_inherited()
global.thewall["player_draw_begin"]=self.depth
```
## draw
```
event_inherited()
global.thewall["player_draw"]=self.depth
```
## draw_end
```
event_inherited()
global.thewall["player_draw_end"]=self.depth
```
## draw_gui_begin
```
event_inherited()
global.thewall["player_draw_gui_begin"]=self.depth
```
## draw_gui
```
event_inherited()
global.thewall["player_draw_gui"]=self.depth
```
## draw_gui_end
```
event_inherited()
global.thewall["player_draw_gui_end"]=self.depth
```
## alarm_0
```
event_inherited()
global.thewall["player_alarm_0"]=self.depth
```
## alarm_1
```
event_inherited()
global.thewall["player_alarm_1"]=self.depth
```
## alarm_2
```
event_inherited()
global.thewall["player_alarm_2"]=self.depth
```
## user_0
```
event_inherited()
global.thewall["player_user_0"]=self.depth
```
## user_1
```
event_inherited()
global.thewall["player_user_1"]=self.depth
```
## user_2
```
event_inherited()
global.thewall["player_user_2"]=self.depth
```
## room_start
```
event_inherited()
global.thewall["player_room_start"]=self.depth
```
## room_end
```
event_inherited()
global.thewall["player_room_end"]=self.depth
```
## destroy
```
event_inherited()
global.thewall["player_destroy"]=self.depth
```
## animation_end
```
event_inherited()
global.thewall["player_animation_end"]=self.depth
```
# enemy
## create
```
global.thewall["enemy_create"]=self.depth
```
## cleanup
```
global.thewall["enemy_cleanup"]=self.depth
```
## step_begin
```
global.thewall["enemy_step_begin"]=self.depth
```
## step
```
global.thewall["enemy_step"]=self.depth
```
## step_end
```
global.thewall["enemy_step_end"]=self.depth
```
## draw_begin
```
global.thewall["enemy_draw_begin"]=self.depth
```
## draw
```
global.thewall["enemy_draw"]=self.depth
```
## draw_end
```
global.thewall["enemy_draw_end"]=self.depth
```
## draw_gui_begin
```
global.thewall["enemy_draw_gui_begin"]=self.depth
```
## draw_gui
```
global.thewall["enemy_draw_gui"]=self.depth
```
## draw_gui_end
```
global.thewall["enemy_draw_gui_end"]=self.depth
```
## alarm_0
```
global.thewall["enemy_alarm_0"]=self.depth
```
## alarm_1
```
global.thewall["enemy_alarm_1"]=self.depth
```
## alarm_2
```
global.thewall["enemy_alarm_2"]=self.depth
```
## user_0
```
global.thewall["enemy_user_0"]=self.depth
```
## user_1
```
global.thewall["enemy_user_1"]=self.depth
```
## user_2
```
global.thewall["enemy_user_2"]=self.depth
```
## room_start
```
global.thewall["enemy_room_start"]=self.depth
```
## room_end
```
global.thewall["enemy_room_end"]=self.depth
```
## destroy
```
global.thewall["enemy_destroy"]=self.depth
```
## animation_end
```
global.thewall["enemy_animation_end"]=self.depth
```
# hitbox
## create
```
global.thewall["hitbox_create"]=self.depth
```
## cleanup
```
global.thewall["hitbox_cleanup"]=self.depth
```
## step_begin
```
global.thewall["hitbox_step_begin"]=self.depth
```
## step
```
global.thewall["hitbox_step"]=self.depth
```
## step_end
```
global.thewall["hitbox_step_end"]=self.depth
```
## draw_begin
```
global.thewall["hitbox_draw_begin"]=self.depth
```
## draw
```
global.thewall["hitbox_draw"]=self.depth
```
## draw_end
```
global.thewall["hitbox_draw_end"]=self.depth
```
## draw_gui_begin
```
global.thewall["hitbox_draw_gui_begin"]=self.depth
```
## draw_gui
```
global.thewall["hitbox_draw_gui"]=self.depth
```
## draw_gui_end
```
global.thewall["hitbox_draw_gui_end"]=self.depth
```
## alarm_0
```
global.thewall["hitbox_alarm_0"]=self.depth
```
## alarm_1
```
global.thewall["hitbox_alarm_1"]=self.depth
```
## alarm_2
```
global.thewall["hitbox_alarm_2"]=self.depth
```
## user_0
```
global.thewall["hitbox_user_0"]=self.depth
```
## user_1
```
global.thewall["hitbox_user_1"]=self.depth
```
## user_2
```
global.thewall["hitbox_user_2"]=self.depth
```
## room_start
```
global.thewall["hitbox_room_start"]=self.depth
```
## room_end
```
global.thewall["hitbox_room_end"]=self.depth
```
## destroy
```
global.thewall["hitbox_destroy"]=self.depth
```
## animation_end
```
global.thewall["hitbox_animation_end"]=self.depth
```
