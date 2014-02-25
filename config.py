# -*- coding: utf8 -*-

from libqtile.config import Key, Screen, Group
from libqtile.command import lazy
from libqtile import layout, bar, widget
import sh

def ensure_running(proc_name, run_proc):
  def start_if_required():
    try:
      sh.pidof(proc_name)
    except sh.ErrorReturnCode:
      run_proc()
  return start_if_required

startup_apps = [lambda: sh.xrandr(s='1920x1080'),
                ensure_running("gnome-settings-daemon",
                               lambda: sh.gnome_settings_daemon(_bg=True)),
                ensure_running("launchy", lambda: sh.launchy(_bg=True)),
                lambda: sh.dropbox("start", _bg=True)]

mod = "mod4"

keys = [
    # Log out
    Key([mod, "control"], "Escape", lazy.shutdown()),

    # Run shortcuts
    Key([mod], "t", lazy.spawn("gnome-terminal")),
    Key([mod], "h", lazy.spawn("thunar")),
    Key([mod], "c", lazy.spawn("google-chrome")),
    Key([mod], "v", lazy.spawn("gvim")),
    Key([mod], "r", lazy.spawncmd()),
    
    # Quit window
    Key([mod], "q", lazy.window.kill()),


    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "Return", lazy.spawn("xterm")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab",    lazy.nextlayout()),
    Key([mod], "w",      lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
]

groups = [
    Group("1"),
    Group("2"),
    Group("3"),
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
]
for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

dgroups_key_binder = None
dgroups_app_rules = []

layouts = [
    layout.Max(),
    layout.Stack(stacks=2)
]

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Sep(),
                widget.TaskList(),
                widget.Sep(),
                widget.Prompt(),
                widget.Notify(),
                widget.Systray(),
                widget.Battery(battery_name='BAT1',
                               energy_now_file='charge_now',
                               energy_full_file='charge_full',
                               power_now_file='current_now',
                               update_delay=1,
                               charge_char=u"↑",
                               discharge_char=u"↓",
                               format='{char} {percent:2.0%}'),
                widget.Clock('%Y-%m-%d %a %I:%M %p'),
            ],
            26,
        ),
    ),
]

def main(qtile):
  for start_app in startup_apps:
    start_app()

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
mouse = ()
auto_fullscreen = True
widget_defaults = {}
