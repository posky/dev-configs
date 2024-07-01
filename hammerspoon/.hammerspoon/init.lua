-- Spoons

-- reload coufiguration
hs.loadSpoon("ReloadConfiguration")
spoon.ReloadConfiguration:start()

-- mouse follow application focus
hs.loadSpoon("MouseFollowsFocus")
spoon.MouseFollowsFocus:start()

-- foundation_remapping
local FRemap = require("foundation_remapping")
local remapper = FRemap.new()
-- syntax
-- :remap(fromKey, toKey)
remapper:remap("rcmd", "f18")
remapper:remap(0x39, "lctrl")
remapper:register()

-- escape key mapping for vim
local input_eng = "com.apple.keylayout.ABC"
-- local input_eng = "com.apple.keylayout.UnicodeHexInput"
local esc_bind

function convert_to_eng()
  local cur_input = hs.keycodes.currentSourceID()
  if not (cur_input == input_eng) then
    -- hs.eventtap.keyStroke({}, "right")
    hs.keycodes.currentSourceID(input_eng)
  end
  esc_bind:disable()
  hs.eventtap.keyStroke({}, "escape")
  esc_bind:enable()
end

esc_bind = hs.hotkey.new({}, "escape", convert_to_eng):enable()
