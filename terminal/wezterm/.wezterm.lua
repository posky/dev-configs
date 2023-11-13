-- Pull in the wezterm API
local wezterm = require("wezterm")

-- This table will hold the configuration.
local config = {}

-- In newer versions of wezterm, use the config_builder which will
-- help provide clearer error messages
if wezterm.config_builder then
	config = wezterm.config_builder()
end

-- This is where you actually apply your config choices

-- https://wezfurlong.org/wezterm/colorschemes/index.html
config.color_scheme = "Snazzy"

-- https://wezfurlong.org/wezterm/config/launch.html#the-launcher-menu

-- https://wezfurlong.org/wezterm/config/fonts.html
config.font = wezterm.font_with_fallback({
	"Hack Nerd Font",
	"DejaVuSansM Nerd Font",
	"Hack",
	"DejaVu Sans Mono",
})

-- and finally, return the configuration to wezterm
return config
