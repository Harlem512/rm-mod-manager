<!-- Rusted Moss Mod Loader. Please don't add this to the rmml modlist -->
<!-- Exposes mod information to the `global.rmml` struct -->
# config

## method

file_text_open_read
file_text_eof
file_text_readln
file_text_close
ds_map_create
ds_map_find_value
ds_map_set

# controller

## create

````js
if (!global.rmml) {
  global.rmml = {}
  global.rmml.version = "3.0"
}

// build mod list
let modlist = []
let f = file_text_open_read('mods/rmml/modlist.txt')
while (!file_text_eof(f)) {
  let mod = string(string_trim(file_text_readln(f)))
  if (
    !string_starts_with(mod, '#') &&
    string_length(mod) > 3 &&
    string_ends_with(mod, '.md') > 0
  ) {
    array_push(modlist, mod)
  }
}
file_text_close(f)

// external modlist
global.rmml.mod_list = []

// internal modmap
global.rmml.modmap = ds_map_create()

// mod loader function
global.rmml.load = function (obj, event, mod_name, catspeak) {
  let obj_event = obj + '_events_' + event
  let event_ar = ds_map_find_value(global.rmml.modmap, obj_event)
  if (event_ar == undefined) {
    event_ar = []
  }
  array_push(event_ar, [mod_name, catspeak])
  ds_map_set(global.rmml.modmap, obj_event, event_ar)
}

// executes the passed event on the object that called it
global.rmml.exec = function (event_name) {
  let is_controller = string_starts_with(event_name, 'controller')
  let is_player = string_starts_with(event_name, 'player')
  // if this instance isn't a controller and hasn't called its create, do that first
  if (!is_controller && !self.rmml_created) {
    self.rmml_created = true
    // call the create event on this object
    let new_event = string(string_split(event_name, '_')[0]) + '_events_create'
    global.rmml.exec(new_event)
  }

  // check if we have events to run
  let mod_cs = ds_map_find_value(global.rmml.modmap, event_name)
  if (mod_cs == undefined) {
    return
  }
  // loop over all registered events
  let i = 0
  while (i < array_length(mod_cs)) {
    // unpack modid and code
    let elem = mod_cs[i]
    let _mod_name = elem[0]
    let _catspeak = elem[1]

    // controllers and players get to speedrun their code
    if (is_controller || is_player) {
      _catspeak()
    // no mod_name set
    } else if (self.mod_name == undefined) {
      // create events get a pass, since they don't have mod_names set yet,
      // unless this is the manual create event
      if (!string_ends_with(event_name, 'create') || self.rmml_created == true) {
        // this throws a runtime exception
        NON_CONTROLLER_INSTANCES_MUST_HAVE_A___mod_name__()
      }
    // run our code if the mod_names match
    } else if (self.mod_name == _mod_name) {
      _catspeak()
    }
    i += 1
  }
}

// load all of the mods
let i = 0
while (i < array_length(modlist)) {
  let mod_name = string(string_split(modlist[i], '.md')[0])
  let mod_file = file_text_open_read('mods/rmml/' + modlist[i])
  array_push(global.rmml.mod_list, mod_name)
  let obj = undefined
  let event = undefined
  let code = ''
  // 0: false, 1: default, 2: js parser
  let code_mode = 0
  let in_config = false
  let config_h2 = undefined
  let in_comment = false

  while (!file_text_eof(mod_file)) {
    let line = string(string_trim(file_text_readln(mod_file)))

    // empty lines get skipped
    if (string_length(line) == 0) {
      continue
    }

    // comment handler
    if (in_comment) {
      if (string_ends_with(line, '-->')) {
        in_comment = false
      }
    // we're in code mode
    } else if (code_mode != 0) {
      if (string_starts_with(line, '```')) {
        // sanity checks
        if (obj == undefined) {
          missingObjectHeaderForCodeBlock()
        }
        if (event == undefined) {
          missingEventHeaderForCodeBlock()
        }
        if (string_length(code) != 0) {
          // parse, compile, and register catspeak
          let parsed = global.__catspeak__.parseString(code)
          let compiled = global.__catspeak__.compile(parsed)
          global.rmml.load(obj, event, mod_name, compiled)
        }
        // end of code
        code = ''
        code_mode = 0
      } else {
        // append the codes
        if (code_mode == 1) {
          code += line + '\n'
        } else {
          // skip js comments
          if (!string_starts_with(line, '//')) {
            // replace js syntax with catspeak syntax
            // the underscores are to prevent my code generator from
            // replacing these with their catspeak equivalents
            let modified = string_replace(line, '__function(__', 'fun(')
            modified = string_replace(modified, '__type(__', 'typeof(')
            modified = string_replace(modified, '__&&__', ' and ')
            modified = string_replace(modified, '__||__', ' or ')
            code += modified + '\n'
          }
        }
      }
    // h1, either config or an object
    } else if (string_starts_with(line, '# ')) {
      let h1 = string_split(line, '# ')[1]
      if (h1 == 'config') {
        in_config = true
      } else {
        in_config = false
        obj = h1
      }
    // h2, some event handler or a configuration thing
    } else if (string_starts_with(line, '## ')) {
      let h2 = string_split(line, '# ')[1]
      if (in_config) {
        config_h2 = h2
      } else {
        event = h2
      }
    // js code block
    } else if (string_starts_with(line, '```js')) {
      code_mode = 2
    // catspeak code block
    } else if (string_starts_with(line, '```')) {
      code_mode = 1
    } else if (string_starts_with(line, '<!--')) {
      // catch one line comments
      in_comment = !string_ends_with(line, '-->')
    // configuration settings
    } else if (in_config) {
      if (config_h2 == 'asset') {
        global.__catspeak__.interface.exposeAsset(line)
      } else if (config_h2 == 'method') {
        global.__catspeak__.interface.exposeMethodByName(line)
      }
      // constants don't work currently
      // function doesn't do anything i guess ??
    }
  }

  file_text_close(mod_file)

  i += 1
}
// run other mod's controller_create code
with (self) {
  global.rmml.exec('controller_events_create')
}
````

<!--
THE FOLLOWING CODE WAS AUTOMATICALLY GENERATED (no i didn't type out the same thing 200 times) wow look its the python source code:

objects = ['controller', 'instance', 'basic', 'player', 'enemy', 'hitbox']
events = ['create', 'cleanup', 'step_begin', 'step', 'step_end', 'draw_begin', 'draw', 'draw_end', 'draw_gui_begin', 'draw_gui', 'draw_gui_end', 'alarm_0', 'alarm_1', 'alarm_2', 'user_0', 'user_1', 'user_2', 'room_start', 'room_end', 'destroy', 'animation_end']

for o in objects:
  if o != 'controller':
    print(f'# {o}')
  for e in events:
    if not (e == 'create' or (e == 'cleanup' and (o == 'basic' or o == 'enemy' or o == 'hitbox'))):
      print(f'## {e}\n```\nwith(self){{global.rmml.exec("{o}_events_{e}")}}\n```')
-->
## cleanup
```
with(self){global.rmml.exec("controller_events_cleanup")}
```
## step_begin
```
with(self){global.rmml.exec("controller_events_step_begin")}
```
## step
```
with(self){global.rmml.exec("controller_events_step")}
```
## step_end
```
with(self){global.rmml.exec("controller_events_step_end")}
```
## draw_begin
```
with(self){global.rmml.exec("controller_events_draw_begin")}
```
## draw
```
with(self){global.rmml.exec("controller_events_draw")}
```
## draw_end
```
with(self){global.rmml.exec("controller_events_draw_end")}
```
## draw_gui_begin
```
with(self){global.rmml.exec("controller_events_draw_gui_begin")}
```
## draw_gui
```
with(self){global.rmml.exec("controller_events_draw_gui")}
```
## draw_gui_end
```
with(self){global.rmml.exec("controller_events_draw_gui_end")}
```
## alarm_0
```
with(self){global.rmml.exec("controller_events_alarm_0")}
```
## alarm_1
```
with(self){global.rmml.exec("controller_events_alarm_1")}
```
## alarm_2
```
with(self){global.rmml.exec("controller_events_alarm_2")}
```
## user_0
```
with(self){global.rmml.exec("controller_events_user_0")}
```
## user_1
```
with(self){global.rmml.exec("controller_events_user_1")}
```
## user_2
```
with(self){global.rmml.exec("controller_events_user_2")}
```
## room_start
```
with(self){global.rmml.exec("controller_events_room_start")}
```
## room_end
```
with(self){global.rmml.exec("controller_events_room_end")}
```
## destroy
```
with(self){global.rmml.exec("controller_events_destroy")}
```
## animation_end
```
with(self){global.rmml.exec("controller_events_animation_end")}
```
# instance
## cleanup
```
with(self){global.rmml.exec("instance_events_cleanup")}
```
## step_begin
```
with(self){global.rmml.exec("instance_events_step_begin")}
```
## step
```
with(self){global.rmml.exec("instance_events_step")}
```
## step_end
```
with(self){global.rmml.exec("instance_events_step_end")}
```
## draw_begin
```
with(self){global.rmml.exec("instance_events_draw_begin")}
```
## draw
```
with(self){global.rmml.exec("instance_events_draw")}
```
## draw_end
```
with(self){global.rmml.exec("instance_events_draw_end")}
```
## draw_gui_begin
```
with(self){global.rmml.exec("instance_events_draw_gui_begin")}
```
## draw_gui
```
with(self){global.rmml.exec("instance_events_draw_gui")}
```
## draw_gui_end
```
with(self){global.rmml.exec("instance_events_draw_gui_end")}
```
## alarm_0
```
with(self){global.rmml.exec("instance_events_alarm_0")}
```
## alarm_1
```
with(self){global.rmml.exec("instance_events_alarm_1")}
```
## alarm_2
```
with(self){global.rmml.exec("instance_events_alarm_2")}
```
## user_0
```
with(self){global.rmml.exec("instance_events_user_0")}
```
## user_1
```
with(self){global.rmml.exec("instance_events_user_1")}
```
## user_2
```
with(self){global.rmml.exec("instance_events_user_2")}
```
## room_start
```
with(self){global.rmml.exec("instance_events_room_start")}
```
## room_end
```
with(self){global.rmml.exec("instance_events_room_end")}
```
## destroy
```
with(self){global.rmml.exec("instance_events_destroy")}
```
## animation_end
```
with(self){global.rmml.exec("instance_events_animation_end")}
```
# basic
## step_begin
```
with(self){global.rmml.exec("basic_events_step_begin")}
```
## step
```
with(self){global.rmml.exec("basic_events_step")}
```
## step_end
```
with(self){global.rmml.exec("basic_events_step_end")}
```
## draw_begin
```
with(self){global.rmml.exec("basic_events_draw_begin")}
```
## draw
```
with(self){global.rmml.exec("basic_events_draw")}
```
## draw_end
```
with(self){global.rmml.exec("basic_events_draw_end")}
```
## draw_gui_begin
```
with(self){global.rmml.exec("basic_events_draw_gui_begin")}
```
## draw_gui
```
with(self){global.rmml.exec("basic_events_draw_gui")}
```
## draw_gui_end
```
with(self){global.rmml.exec("basic_events_draw_gui_end")}
```
## alarm_0
```
with(self){global.rmml.exec("basic_events_alarm_0")}
```
## alarm_1
```
with(self){global.rmml.exec("basic_events_alarm_1")}
```
## alarm_2
```
with(self){global.rmml.exec("basic_events_alarm_2")}
```
## user_0
```
with(self){global.rmml.exec("basic_events_user_0")}
```
## user_1
```
with(self){global.rmml.exec("basic_events_user_1")}
```
## user_2
```
with(self){global.rmml.exec("basic_events_user_2")}
```
## room_start
```
with(self){global.rmml.exec("basic_events_room_start")}
```
## room_end
```
with(self){global.rmml.exec("basic_events_room_end")}
```
## destroy
```
with(self){global.rmml.exec("basic_events_destroy")}
```
## animation_end
```
with(self){global.rmml.exec("basic_events_animation_end")}
```
# player
## cleanup
```
with(self){global.rmml.exec("player_events_cleanup")}
```
## step_begin
```
with(self){global.rmml.exec("player_events_step_begin")}
```
## step
```
with(self){global.rmml.exec("player_events_step")}
```
## step_end
```
with(self){global.rmml.exec("player_events_step_end")}
```
## draw_begin
```
with(self){global.rmml.exec("player_events_draw_begin")}
```
## draw
```
with(self){global.rmml.exec("player_events_draw")}
```
## draw_end
```
with(self){global.rmml.exec("player_events_draw_end")}
```
## draw_gui_begin
```
with(self){global.rmml.exec("player_events_draw_gui_begin")}
```
## draw_gui
```
with(self){global.rmml.exec("player_events_draw_gui")}
```
## draw_gui_end
```
with(self){global.rmml.exec("player_events_draw_gui_end")}
```
## alarm_0
```
with(self){global.rmml.exec("player_events_alarm_0")}
```
## alarm_1
```
with(self){global.rmml.exec("player_events_alarm_1")}
```
## alarm_2
```
with(self){global.rmml.exec("player_events_alarm_2")}
```
## user_0
```
with(self){global.rmml.exec("player_events_user_0")}
```
## user_1
```
with(self){global.rmml.exec("player_events_user_1")}
```
## user_2
```
with(self){global.rmml.exec("player_events_user_2")}
```
## room_start
```
with(self){global.rmml.exec("player_events_room_start")}
```
## room_end
```
with(self){global.rmml.exec("player_events_room_end")}
```
## destroy
```
with(self){global.rmml.exec("player_events_destroy")}
```
## animation_end
```
with(self){global.rmml.exec("player_events_animation_end")}
```
# enemy
## step_begin
```
with(self){global.rmml.exec("enemy_events_step_begin")}
```
## step
```
with(self){global.rmml.exec("enemy_events_step")}
```
## step_end
```
with(self){global.rmml.exec("enemy_events_step_end")}
```
## draw_begin
```
with(self){global.rmml.exec("enemy_events_draw_begin")}
```
## draw
```
with(self){global.rmml.exec("enemy_events_draw")}
```
## draw_end
```
with(self){global.rmml.exec("enemy_events_draw_end")}
```
## draw_gui_begin
```
with(self){global.rmml.exec("enemy_events_draw_gui_begin")}
```
## draw_gui
```
with(self){global.rmml.exec("enemy_events_draw_gui")}
```
## draw_gui_end
```
with(self){global.rmml.exec("enemy_events_draw_gui_end")}
```
## alarm_0
```
with(self){global.rmml.exec("enemy_events_alarm_0")}
```
## alarm_1
```
with(self){global.rmml.exec("enemy_events_alarm_1")}
```
## alarm_2
```
with(self){global.rmml.exec("enemy_events_alarm_2")}
```
## user_0
```
with(self){global.rmml.exec("enemy_events_user_0")}
```
## user_1
```
with(self){global.rmml.exec("enemy_events_user_1")}
```
## user_2
```
with(self){global.rmml.exec("enemy_events_user_2")}
```
## room_start
```
with(self){global.rmml.exec("enemy_events_room_start")}
```
## room_end
```
with(self){global.rmml.exec("enemy_events_room_end")}
```
## destroy
```
with(self){global.rmml.exec("enemy_events_destroy")}
```
## animation_end
```
with(self){global.rmml.exec("enemy_events_animation_end")}
```
# hitbox
## step_begin
```
with(self){global.rmml.exec("hitbox_events_step_begin")}
```
## step
```
with(self){global.rmml.exec("hitbox_events_step")}
```
## step_end
```
with(self){global.rmml.exec("hitbox_events_step_end")}
```
## draw_begin
```
with(self){global.rmml.exec("hitbox_events_draw_begin")}
```
## draw
```
with(self){global.rmml.exec("hitbox_events_draw")}
```
## draw_end
```
with(self){global.rmml.exec("hitbox_events_draw_end")}
```
## draw_gui_begin
```
with(self){global.rmml.exec("hitbox_events_draw_gui_begin")}
```
## draw_gui
```
with(self){global.rmml.exec("hitbox_events_draw_gui")}
```
## draw_gui_end
```
with(self){global.rmml.exec("hitbox_events_draw_gui_end")}
```
## alarm_0
```
with(self){global.rmml.exec("hitbox_events_alarm_0")}
```
## alarm_1
```
with(self){global.rmml.exec("hitbox_events_alarm_1")}
```
## alarm_2
```
with(self){global.rmml.exec("hitbox_events_alarm_2")}
```
## user_0
```
with(self){global.rmml.exec("hitbox_events_user_0")}
```
## user_1
```
with(self){global.rmml.exec("hitbox_events_user_1")}
```
## user_2
```
with(self){global.rmml.exec("hitbox_events_user_2")}
```
## room_start
```
with(self){global.rmml.exec("hitbox_events_room_start")}
```
## room_end
```
with(self){global.rmml.exec("hitbox_events_room_end")}
```
## destroy
```
with(self){global.rmml.exec("hitbox_events_destroy")}
```
## animation_end
```
with(self){global.rmml.exec("hitbox_events_animation_end")}
```
