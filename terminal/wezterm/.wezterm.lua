-- Pull in the wezterm API
local wezterm = require("wezterm")
local act = wezterm.action

wezterm.on("update-right-status", function(window, pane)
	window:set_right_status(window:active_workspace())
end)

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
config.window_background_opacity = 0.95

-- https://wezfurlong.org/wezterm/config/launch.html#the-launcher-menu

-- https://wezfurlong.org/wezterm/config/fonts.html
config.font = wezterm.font_with_fallback({
	"Hack Nerd Font",
	"DejaVuSansM Nerd Font",
	"Hack",
	"DejaVu Sans Mono",
})

-- keybindings
config.keys = {
	-- Switch to the default active_workspace
	{
		key = "y",
		mods = "CTRL|SHIFT",
		action = act.SwitchToWorkspace({
			name = "default",
		}),
	},
	-- Create a new workspace with a random name and switch to it
	{
		key = "i",
		mods = "CTRL|SHIFT",
		action = act.PromptInputLine({
			description = wezterm.format({
				{ Attribute = { Intensity = "Bold" } },
				{ Foreground = { AnsiColor = "Fuchsia" } },
				{ Text = "Enter name for new workspace" },
			}),
			action = wezterm.action_callback(function(window, pane, line)
				-- line will be 'nil' if they hit escape without entering anything
				-- An empty string if they just hit enter
				-- Or the actual line of text they wrote
				if line then
					window:perform_action(
						act.SwitchToWorkspace({
							name = line,
						}),
						pane
					)
				end
			end),
		}),
	},
	{ key = "1", mods = "ALT", action = act.ShowLauncher },
	-- Show the launcher in fuzzy selection mode and have it list all workspaces
	-- and allow activating one.
	{
		key = "9",
		mods = "ALT",
		action = act.ShowLauncherArgs({
			flags = "FUZZY|WORKSPACES",
		}),
	},
}

-- and finally, return the configuration to wezterm
return config
