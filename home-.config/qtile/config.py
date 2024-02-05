# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c sset Master 1+ unmute")),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_width=3, margin=8, border_focus="#81a1c1", border_normal="#2e3440"),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="RobotoMono Nerd Font",
    fontsize=15,
    padding=3,
)
extension_defaults = widget_defaults.copy()

powerline = {
    "decorations": [
        PowerLineDecoration(path='arrow_right')
    ]
}

screens = [
    Screen(
        top=bar.Bar(
            [
		widget.Sep(
                    linewidth = 1,
                    padding = 5,
                    foreground = "#4c566a",
                    background = "#2e3440"
                ),
                widget.CurrentLayoutIcon(
                    padding = 4,
                    scale = 0.7,
                    foreground = "#d8dee9",
                    background = "#2e3440"
                ),
                 widget.Sep(
                    linewidth = 1,
                    padding = 5,
                    foreground = "#4c566a",
                    background = "#2e3440"
                ),
                widget.GroupBox(
                    font = "RobotoMono Nerd Font Bold",
                    fontsize = 16,
                    margin_y = 2,
                    margin_x = 0,
                    padding_y = 5,
                    padding_x = 3,
                    borderwidth = 3,
                    disable_drag = True,
                    active = "#4c566a",
                    inactive = "#8994a9",
                    rounded = False,
		    #highlight_color="#AF656E",
                    highlight_method = "line",
                    this_current_screen_border ="#C68B7B",
		    this_screen_border="#ff4d4d",
		    other_current_screen_border="#E4C890",
		    other_screen_border="#A789A6",
                    foreground = "#4c566a",
                    background = "#2e3440"
                ),
                 widget.Sep(
                    linewidth = 1,
                    padding = 5,
                    foreground = "#4c566a",
                    background = "#2e3440"
                ),
                widget.Prompt(
                    foreground = "#d8dee9",
                    background = "#2e3440",
                    padding = 5,
                    linewidth = 1
                ),
                widget.WindowName(
                    font = "RobotoMono Nerd Font Bold",
                    fontsize = 16,
                    foreground = "#d8dee9",
                    background = "#2e3440",
                    **powerline,
                ),
  		#widget.Sep(
                    #foreground = "#4c566a",
                    #background = "#2e3440",
                    #padding = 5,
                    #linewidth = 1
                #),
		#widget.TextBox(
		    #text='◁',
		    #padding=0,
    		    #foreground=["#FFFFFF"],
		    #background="#AF656E",
		    #fontsize=27
		#),
		widget.Net(
                    foreground = "#2e3440",
                    background = "#AF656E",
                    font = 'RobotoMono Nerd Font Bold',
                    fontsize = 13,
                    format = '{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}',
                    interface = 'wlp3s0',
		    **powerline,
                ),
		#widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #foreground = "#4c566a",
                    #background = "#2e3440"
                #),
		widget.CPU(
                    background = "#C68B7B",
                    foreground = "#2e3440",
                    font = "RobotoMono Nerd Font Bold",
                    fontsize = 13,
                    **powerline,
                ),
                #widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #foreground = "4c566a",
                    #background = "#2e3440"
                #),
		widget.Memory(
                    measure_mem = 'G',
                    foreground = "#2e3440",
                    background = "#ff4d4d",
                    font = "RobotoMono Nerd Font Bold",
                    fontsize = 13,
                    **powerline,
                ),
                #widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #foreground = "#4c566a",
                    #background = "#2e3440"
                #),
		widget.DF(
                    visible_on_warn = False,
                    background = "#E4C890",
                    foreground = "#2e3440",
                    font = "RobotoMono Nerd Font Bold",
                    fontsize = 13,
                    **powerline,
                ),
                #widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #background = "#2e3440",
                    #foreground = "#4c566a"
                #),
		widget.Clock(
                    foreground = "#2e3440",
                    background = "#A789A6",
                    font = "RobotoMono Nerd Font Bold",
                    fontsize = 13,
                    format = "%a, %d %b - %H:%M",
                    **powerline,
                ),
		#widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #foreground = "#4c566a",
                    #background = "#2e3440"
                #),
		widget.Systray(
 		    background = "#FF0000",
                    icon_size = 20,
                    padding = 5,
                    **powerline,
                ),
                #widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #foreground = "#4c566a",
                    #background = "#2e3440" 
                #),
		widget.OpenWeather(
                    app_key = "4cf3731a25d1d1f4e4a00207afd451a2",
                    cityid = "1268782",
                    location = 'Jalandhar, IN',
		    format = '{location_city}: {main_temp}° {icon}  {humidity}%  {weather_details}',
                    metric = True,
                    font = "RobotoMono Nerd Font Bold",
                    fontsize = 13,
                    background = "#789BB1",
                    foreground = "#2e3440",
                    **powerline,
                ),
                #widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #background = "#2e3440",
                    #foreground = "#4c566a"
                #),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("default config", name="default"),
                #widget.TextBox("Jai Shree Ram", foreground="#d75f5f"),
		widget.Battery(
		    battery="BAT0", 
                    background="#A4B797", 
                    font="RobotoMono Nerd Font Bold", 
                    fontsize=13, 
                    foreground="#2e3440",
		    format='{char} {percent:2.0%}',
		    charge_char='^',
   	 	    discharge_char='v',
		    full_char='%',
		    low_background='#ff0000',
		    padding=5,
		    notify_below=68,
                    **powerline,
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
		#widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #background = "#2e3440",
                    #foreground = "#4c566a"
                #),
		#widget.Volume(
		    #background="#6691DE",
		    #foreground="#2e3440",
		    #channel="IEC958",
		    #font="RobotoMono Nerd Font Bold",
		    #fontsize=13,
		    #padding=5,
		#),
		#widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #background = "#2e3440",
                    #foreground = "#4c566a"
                #),
                widget.QuickExit(
                    background="#9D7CB9",
		    foreground="#2e3440",
		    default_text="Power",
		    padding=5,
		    fontsize=13,
		    font="RobotoMono Nerd Font Bold",
		),
		#widget.Sep(
                    #linewidth = 1,
                    #padding = 5,
                    #background = "#2e3440",
                    #foreground = "#4c566a"
                #),
            ],
            24,
	    #background=["#00000000"],
	    margin=[10, 0, 0, 0],
            #border_width=[15, 0, 15, 0],  # Draw top and bottom borders
            #border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])
