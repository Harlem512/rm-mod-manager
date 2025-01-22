Rusted Moss Mod Manager

```sp
global.component = {
  click_inside: fun (x,y, w,h) {
    return mouse_check_button_pressed(mb_left)
      and point_in_rectangle(global.mousex, global.mousey,
        x, y,
        x + w, y + h)
  },
  label: fun (x, y, w, h, text, hover, hover_text) {
    let pin = if hover {
      point_in_rectangle(global.mousex, global.mousey,
        x, y,
        x + w, y + h
      )
    }

    draw_sprite_stretched_ext(sui_9slice, 0, x, y, w, h,
      if pin {c_ltgray} else {c_white}, 1)
    if text != undefined {
      draw_text(x + 6, y + 6, text)
    }

    -- tool tip in bottom right
    if pin and hover_text != undefined {
      global.component.label(2, 226,
        string_length(hover_text) * 6 + 24, 22,
        hover_text)
    }

    return pin
  },
  button: fun (x, y, w, h, text, hover_text) {
    let click = global.component.label(x, y, w, h, text, true, hover_text)
        and mouse_check_button_pressed(mb_left)

    if click {
      audio_play_sound_volume(snd_menu_1, 1, 1)
    }

    return click
  },
}

-- parse json
global.parse_json_file = fun (filename) {
  return global.rmml.try_catch(fun (filename) {
    b = buffer_load(filename)
    s = buffer_read(b, buffer_string)
    buffer_delete(b)
    return json_parse(s)
  }, undefined, filename)
}
```

# controller

## create

```sp
-- RMMM version
self.version = 0.3
-- manifest url
-- DEBUG: test server
-- self.manifest_url = "http://127.0.0.1:8080/manifest.json"
self.manifest_url = "https://raw.githubusercontent.com/Harlem512/rm-mod-database/refs/heads/main/manifest.json"

self.manifest_file = "mods/rmmm/manifest.json"
self.depth = 0
-- rendering state
-- -3: confirm RMMM reset
-- -2: confirm mod delete
-- -1: confirm save
--  0: settings icon
--  1: installed mods
--  2: browse mods
--  3: download manifest
--  4: render game folder
--  5: render save folder
self.state = 0
-- scroll for mod lists
self.scroll = 0
-- if we should show the full mod list on the main menu
self.show_full_list = true
-- true if we're downloading the foreign manifest
self.downloading_manifest = undefined
-- true if we must force a restart
self.force_restart = false

-- true if a mod is being downloaded
self.downloading_mod = false
-- builds transformed foreign manifest
self.transform_foreign_manifest = fun () {
  let names = struct_get_names(self.foreign_manifest)
  array_sort(names, true)
  self.foreign_manifest_list = []
  let j = 0
  while j < array_length(names) {
    let mod_name = names[j]
    let meta = self.foreign_manifest[mod_name]
    let local = self.local_manifest[mod_name]
    if local {
      meta._local = local.version
    }
    array_push(self.foreign_manifest_list, meta)
    j += 1
  }
}

-- temporary downloads
self.directory = fun (file) {
  return temp_directory_get() + "rmmm/" + file
}

-- -----------------------------------------------------------------------------
--                            cache local manifest
-- -----------------------------------------------------------------------------
self.cache_local = fun () {
  -- raw manifest
  let raw_manifest = {}
  if file_exists(self.manifest_file) {
    raw_manifest = global.parse_json_file(self.manifest_file)
    if !raw_manifest {
      global.rmml.warnings += "| Parsing error with local manifest, resetting"
      file_delete(self.manifest_file)
      raw_manifest = {}
    }
  }
  if !raw_manifest["rmml.meow"] {
    raw_manifest["rmml.meow"] = {
      name: "rmml.meow",
      display: "Rusted Moss Mod Loader",
      description: "Invisible middleware that loads mods\n(It's already installed)",
      author: "Harlem512",
      version: global.rmml.version,
      type: "meow",
    }
  }
  if !raw_manifest["rmmm.md"] {
    raw_manifest["rmmm.md"] = {
      name: "rmmm.md",
      display: "Rusted Moss Mod Manager",
      description: "Manages mod installations and downloads mods.",
      author: "Harlem512",
      version: self.version,
      type: "md",
    }
  }

  -- rebuild the local manifest, based on what's actually installed
  self.local_manifest = {}
  let local_mods = []
  -- 16: include directories
  let mod = file_find_first("mods/rmml/*", 16)
  while mod != "" {
    array_push(local_mods, mod)
    -- raw manifest exists, use that
    if raw_manifest[mod] {
      self.local_manifest[mod] = raw_manifest[mod]
    } else {
      -- no raw manifest, time to bake
      self.local_manifest[mod] = {
        name: mod,
        display: mod,
        description: "[ Locally installed mod ]",
        version: 0,
        author: "Unknown",
      }
    }
    mod = file_find_next()
  }
  file_find_close()

  -- list of local mods and their data
  self.sorted_local_mods = []

  -- add mods that are on the modlist
  let found_mods = {}
  let f = file_text_open_read("mods/modlist.txt")
  while !file_text_eof(f) {
    let mod_path = string(string_trim(file_text_readln(f)))
    let disabled = false

    if string_starts_with(mod_path, "#") {
      mod_path = string_copy(mod_path, 2, string_length(mod_path))
      disabled = true
    }

    -- rmml is not a mod for the modlist
    if mod_path == "rmml.meow" {
      continue
    }

    -- add mod to the array if it exists locally and hasn't already been added
    let manifest = self.local_manifest[mod_path]
    if !found_mods[mod_path] and manifest {
      found_mods[mod_path] = true
      array_push(self.sorted_local_mods, {
        path: mod_path,
        disabled: disabled,
        manifest: manifest
      })
    }
  }
  file_text_close(f)

  -- add mods that are in the folder, but not known to rmmm's modlist
  let i = 0
  while i < array_length(local_mods) {
    let mod = local_mods[i]
    if !found_mods[mod] and mod != "rmml.meow" {
      array_push(self.sorted_local_mods, {
        path: mod,
        disabled: true,
        manifest: self.local_manifest[mod],
      })
    }
    i += 1
  }
}

self.save_mods = fun () {
  let list = file_text_open_write("mods/modlist.txt")
  file_text_write_string(list, "# put your mods here (or disable them with #)\n# mods are loading (and run) in the order written here\n# this file is also managed by RMMM\n")
  let i = 0
  while i < array_length(self.sorted_local_mods) {
    let mod = self.sorted_local_mods[i]
    if mod.disabled {
      file_text_write_string(list, "#" + mod.path + "\n")
    } else {
      file_text_write_string(list, mod.path + "\n")
    }
    i += 1
  }
  file_text_close(list)
}


self.save_manifest = fun () {
  let manifest = file_text_open_write(self.manifest_file)
  file_text_write_string(manifest, json_stringify(self.local_manifest))
  file_text_close(manifest)
}

-- crash safety valve
if !global.rmml.dev {
  if file_exists("mods/back.modlist.txt") {
    global.rmml.warn("Startup crash detected, disabled mods")
    file_delete("mods/modlist.txt")
    -- file_delete("mods/back.modlist.txt")
  }
  file_rename("mods/modlist.txt", "mods/back.modlist.txt")

  alarm_set(0, 10)
}
```

## alarm_0

```sp
-- renames the modlist
file_rename("mods/back.modlist.txt", "mods/modlist.txt")
```

## draw_end

```sp
let menu = instance_find(omenu_new)

-- unload this mod when we're loading a new save
if !menu or menu.state == 8 {
  global.rmml.unload()
  file_rename("mods/back.modlist.txt", "mods/modlist.txt")
  return
}

-- check state
if menu.state != 14 and menu.state != -512 { return }

let next_state = self.state

let col = draw_get_color()
draw_set_color(c_black)

-- Initial, show mod list and RMMM button
if self.state == 0 {
  -- Modlist
  let w
  let h

  let num_mods = array_length(global.rmml.mod_list)
  if self.show_full_list {
    let max_len = 0
    i = 0
    while i < num_mods {
      max_len = max(max_len, string_length(global.rmml.mod_list[i]))
      i += 1
    }

    w = max_len * 6
    h = num_mods * 10
  } else {
    -- string_length("# Mods: XX")
    w = 60
    h = 10
  }

  -- ---------------------------------------------------------------------------
  --                                rmmm button
  -- ---------------------------------------------------------------------------
  if global.component.button(
    418, 2, 22, 22,
  ) {
    next_state = 1
    menu.state = -512
    self.cache_local()
  }
  draw_sprite_ext(smenu_bar,1, 429,13, 1,1, 0,
    if global.rmml.warnings != "" { c_red } else { c_black }, 1
  )

  -- ---------------------------------------------------------------------------
  --                                 mod list
  -- ---------------------------------------------------------------------------

  let bg_x = 404 - w
  let bg_y = 2
  bg_w = w + 12
  bg_h = h + 12

  draw_sprite_stretched(sui_9slice, 0, bg_x, bg_y, bg_w, bg_h)

  if self.show_full_list {
    i = 0
    while i < num_mods {
      draw_text(bg_x + 6, bg_y + 6 + 10 * i, global.rmml.mod_list[i])
      i += 1
    }
  } else {
    draw_text(bg_x + 6, bg_y + 6, "# Mods: " + string(num_mods))
  }

  if global.component.click_inside(bg_x, bg_y, bg_w, bg_h) {
    self.show_full_list = !self.show_full_list
  }
} else if self.state == -1 {
  -- confirm save
  draw_sprite_stretched(sui_9slice, 0, 54, 64, 336, 88)
  scribble("  Changing your mod list\n    requires restarting\n        Rusted Moss")
      .blend(0, 1)
      .transform(2, 2, 0)
      .draw(60, 70)

  if global.component.button(
    154, 164, 78, 22,
    "Save & Quit",
  ) {
    self.save_mods()
    game_end()
  }

  if global.component.button(
    242, 164, 48, 22,
    "Cancel",
  ) {
    next_state = 1
    self.cache_local()
  }
} else if self.state == -2 {
  -- confirm delete
  draw_sprite_stretched(sui_9slice, 0, 54, 64, 336, 88)
  scribble("   Confirm delete mod:\n" + self.delete_manifest.name)
      .blend(0, 1)
      .transform(2, 2, 0)
      .draw(60, 70)

  if global.component.button(
    154, 164, 78, 22,
    "Delete Mod",
  ) {
    next_state = 1
    -- remove mod from list
    array_delete(self.sorted_local_mods, self.delete_index, 1)
    -- remove mod from manifest
    struct_remove(self.local_manifest, self.delete_manifest.name)
    -- delete mod files
    if self.delete_manifest.type == "zip" {
      -- delete old mod
      directory_destroy("mods/rmml/" + self.delete_manifest.name)
    } else {
      -- delete old mod
      file_delete("mods/rmml/" + self.delete_manifest.name)
    }
    self.save_manifest()
    self.force_restart = true
  }

  if global.component.button(
    242, 164, 48, 22,
    "Cancel",
  ) {
    next_state = 1
  }
-- confirm delete rmmm button
} else if self.state == -3 {
    -- confirm delete
  draw_sprite_stretched(sui_9slice, 0, 54, 34, 336, 118)
  scribble("   Are you sure you want\n    to completely reset\n  Rusted Moss Mod Loader?\n This will remove all mods")
      .blend(0, 1)
      .transform(2, 2, 0)
      .draw(60, 39)

  if global.component.button(
    160, 164, 72, 22,
    "Reset RMMM",
  ) {
    directory_destroy("mods")
    game_end()
  }

  if global.component.button(
    242, 164, 48, 22,
    "Cancel",
  ) {
    next_state = 1
  }
-- main tab is open
} else {
  -- ---------------------------------------------------------------------------
  --                                 main tab
  -- ---------------------------------------------------------------------------
  -- cancel button
  if !self.force_restart {
    if global.component.button(
      394, 2, 48, 22,
      "Cancel",
    ) {
      next_state = 0
      menu.state = 14
    }
  }

  -- save button
  if global.component.button(
    314, 2, 78, 22,
    "Save & Quit",
  ) {
    next_state = -1
  }

  -- background
  draw_sprite_stretched(sui_9slice, 0, 2, 26, 440, 198)

  -- installed mods tab
  if global.component.button(
    6, 2, 96, 22 + (self.state == 1) * 7,
    "Installed Mods",
  ) {
    next_state = 1
    self.cache_local()
    self.scroll = 0
  }

  -- current mods tab
  if global.component.button(
    104, 2, 78, 22 + (self.state == 2 or self.state == 3) * 7,
    "Browse Mods",
  ) {
    if self.foreign_manifest {
      next_state = 2
      self.scroll = 0
    } else {
      next_state = 3
      self.scroll = 0
    }
  }

    -- current mods tab
  if global.component.button(
    209, 2, 78, 22,
    "View Online",
  ) {
    url_open("https://github.com/Harlem512/rm-mod-database")
  }

  if self.state == 3 {
    -- -------------------------------------------------------------------------
    --                            download manifest
    -- -------------------------------------------------------------------------
    if self.downloading_manifest {
      let f = self.directory("foreign_manifest.json")
      if file_exists(f) {
        self.downloading_manifest = false
        self.foreign_manifest = global.parse_json_file(f)
        if !is_struct(self.foreign_manifest) {
          global.rmml.throw("There was an error parsing\nthe foreign manifest\nPlease contact Harlem512 or try again later")
        }
        self.transform_foreign_manifest()
        file_delete(f)
        next_state = 2
      }
      scribble("Downloading manifest...")
        .blend(0, 1)
        .transform(2, 2, 0)
        .draw(78, 70)
    } else {
      scribble("Download manifest\n  to continue")
        .blend(0, 1)
        .transform(2, 2, 0)
        .draw(121, 70)

      if global.component.button(
        192, 164, 60, 22,
        "Download",
      ) {
        self.downloading_manifest = true
        let f = self.directory("foreign_manifest.json")
        file_delete(f)
        http_get_file(self.manifest_url, f)
      }
    }
  } else if self.state == 4 {
    draw_text(8, 38, "This directory contains initial and manually installed mods:")
    scribble(program_directory_get() + "mods")
      .blend(0, 1)
      .fit_to_box(438, 186)
      .draw(8, 60)
  } else if self.state == 5 {
    draw_text(8, 38, "This directory contains mods downloaded by RMMM:")
    scribble(game_save_id_get() + "mods")
      .blend(0, 1)
      .fit_to_box(438, 186)
      .draw(8, 60)
  } else {
    -- -------------------------------------------------------------------------
    --                                list box
    -- -------------------------------------------------------------------------
    let list = if self.state == 1 { self.sorted_local_mods } else { self.foreign_manifest_list }
    let len = array_length(list)

    -- scroll up
    if global.component.button(
      20, 30, 400, 17,
      undefined,
      "Scroll Up"
    ) {
      self.scroll = max(0, self.scroll - 1)
    }
    let i = 0
    while i < 6 {
      draw_sprite_ext(sui_arrow_white_alt,0, 63 + i * 78,39, 1,1, 180, c_black,1)
      i += 1
    }

    -- scroll down
    if global.component.button(
      20, 203, 400, 17,
      undefined,
      "Scroll Down"
    ) {
      self.scroll = min(max(len - 7, 0), self.scroll + 1)
    }
    i = 0
    while i < 6 {
      draw_sprite_ext(sui_arrow_white_alt,0, 63 + i * 78,211, 1,1, 0, c_black,1)
      i += 1
    }

    -- scroll bar
    draw_sprite_stretched(sui_9slice, 0, 6, 30, 10, 190)
    let top = self.scroll / len
    let bot = min(1, 7 / len)
    draw_sprite_stretched_ext(sui_9slice, 0, 6, 30 + top * 190, 10, bot * 190, c_gray, 1)

    -- the table
    let index = self.scroll
    let offset = 0
    let stop = min(len, index + 7)
    let hovered = -1
    while index < stop {
      -- row data
      let mod_meta = list[index]
      -- display offset
      let y = offset + 49
      -- mod label
      let label

      -- INSTALLED MODS
      if self.state == 1 {
        -- enable/disable
        if global.component.button(
          16, y, 17, 22,
          if mod_meta.disabled { "" } else { "X" },
          if mod_meta.disabled { "Enable Mod" } else { "Disable Mod" },
        ) {
          mod_meta.disabled = !mod_meta.disabled
        }

        -- reorder up
        if global.component.button(
          35, y, 18, 22,
          undefined,
          "Load Earlier"
        ) {
          if index != 0 and len > 1 {
            self.sorted_local_mods[index] = self.sorted_local_mods[index - 1]
            self.sorted_local_mods[index - 1] = mod_meta
          }
        }
        draw_sprite_ext(sui_arrow_white_alt,0, 44,y+11, 1,1, 180, c_black,1)

        -- reorder down
        if global.component.button(
          55, y, 18, 22,
          undefined,
          "Load Later"
        ) {
          if index < len - 1 and len > 1 {
            self.sorted_local_mods[index] = self.sorted_local_mods[index + 1]
            self.sorted_local_mods[index + 1] = mod_meta
          }
        }
        draw_sprite_ext(sui_arrow_white_alt,0, 64,y+11, 1,1, 0, c_black,1)

        -- delete
        if global.component.button(
          75, y, 19, 22,
          undefined,
          "Delete Mod"
        ) {
          next_state = -2
          self.delete_index = index
          self.delete_manifest = mod_meta.manifest
        }
        draw_sprite_ext(seditor_delete_button_icon,2, 84,y+10, 1,1, 0, c_black,1)

        label = mod_meta.manifest.display + "  (v" + string(mod_meta.manifest.version) + ")"
      -- BROWSE MODS
      } else {
        -- downloading state check
        if mod_meta._downloading {
          let f = self.directory(mod_meta.name)
          if file_exists(f) {
            -- delete old mod
            directory_destroy("mods/rmml/" + mod_meta.name)
            file_delete("mods/rmml/" + mod_meta.name)
            if mod_meta.type == "zip" {
              -- unzip
              zip_unzip(f, "mods/rmml")
            } else {
              -- copy
              file_copy(f, "mods/rmml/" + mod_meta.name)
            }
            -- delete download
            file_delete(f)
            -- check if mods bricked themselves
            if file_exists("/mods/rmml") {
              global.rmml.warn("rmml folder bricked")
              file_delete("/mods/rmml")
            }
            -- unmark deleted
            mod_meta._downloading = false
            self.downloading_mod = false
            -- update local manifest
            self.local_manifest[mod_meta.name] = {
              name: mod_meta.name,
              display: mod_meta.display,
              description: mod_meta.description,
              author: mod_meta.author,
              version: mod_meta.version,
              type: mod_meta.type,
            }
            mod_meta._local = mod_meta.version
            self.force_restart = true
            -- update local file
            self.save_manifest()
          }

          -- draw loading kid
          draw_sprite(snpc_kids_3, 0,
            46 + sin(current_time_get() / 240 % 314) * 20,y+22
          )
        } else {
          if global.component.button(
            16, y, 80, 22,
            if mod_meta._local == undefined {
              "  Download"
            } else if mod_meta._local < mod_meta.version {
              "   Update"
            } else {
              " Re-install"
            }
          ) and !self.downloading_mod {
            self.downloading_mod = true
            mod_meta._downloading = true
            let f = self.directory(mod_meta.name)
            file_delete(f)
            http_get_file(mod_meta.url, f)
          }
        }

        label = mod_meta.display + "  (v" + string(mod_meta.version) + ")"
      }

      -- render mod name
      if global.component.label(
        96, y, 340, 22,
        label,
        true
      ) {
        if self.state == 1 {
          hovered = mod_meta.manifest
        } else {
          hovered = mod_meta
        }
      }
      index += 1
      offset += 22
    }

    -- 40-character display
    if hovered {
      draw_sprite_stretched(sui_9slice, 0, 190, 26, 252, 198)
      draw_text(196, 32, hovered.display)
      draw_text(196, 44, hovered.name + " (v" + string(hovered.version) + ")  By: " + hovered.author)
      draw_set_color(#58514A)
      draw_line(192, 57, 438, 57)
      draw_set_color(c_black)
      scribble(hovered.description)
        .blend(0, 1)
        .fit_to_box(240, 186)
        .draw(196, 60)
    }
  }

  -- ---------------------------------------------------------------------------
  --                                bottom bar
  -- ---------------------------------------------------------------------------

  -- bottom bar
  if global.rmml.warnings != "" {
    -- render rmml warnings
    if global.component.button(
      2, 226, 440, 22,
      global.rmml.warnings,
    ) {
      show_message(string_replace_all(global.rmml.warnings, "|", "\n"))
    }
  } else {
    -- version info
    draw_sprite_stretched(sui_9slice, 0, 376, 226, 66, 22)
    draw_text(382, 232, "rmml " + string(global.rmml.version))

    -- delete all mods
    if global.component.button(
      302, 226, 72, 22,
      "Reset RMMM",
    ) {
      next_state = -3
    }

    -- game folder
    off = (self.state == 4) * 7
    if global.component.button(
      222, 226 - off, 78, 22 + off
      "Game Folder",
    ) {
      next_state = 4
    }

    -- save folder
    off = (self.state == 5) * 7
    if global.component.button(
      142, 226 - off, 78, 22 + off
      "Save Folder",
    ) {
      next_state = 5
    }
  }
}

self.state = next_state

draw_set_color(col)
```
