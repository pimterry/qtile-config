# -*- coding: utf8 -*-

from libqtile.config import Key, Screen, Group
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import sh

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
mouse = ()
auto_fullscreen = True
widget_defaults = {}

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

def main(qtile):
  for start_app in startup_apps:
    start_app()

@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True

groups = [
    Group("1"),
    Group("2"),
    Group("3"),
    Group("4")
]

dgroups_key_binder = None
dgroups_app_rules = []

layouts = [
    layout.MonadTall(border_width=1, border_focus="#dddddd"),
    layout.Max()
]

screens = [Screen(top=bar.Bar([
                      widget.GroupBox(fontsize=12),
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
                  ], 26, ))]

mod = "mod4"
alt = "mod1"
control = "control"
shift = "shift"

keys = [
    # Log out
    Key([mod, control], "Escape", lazy.shutdown()),

    # Run shortcuts
    Key([mod], "t", lazy.spawn("gnome-terminal")),
    Key([mod], "e", lazy.spawn("thunar")),
    Key([mod], "c", lazy.spawn("google-chrome")),
    Key([mod], "v", lazy.spawn("gvim")),
    Key([mod], "r", lazy.spawncmd()),
    Key([control, mod, alt], "l", lazy.spawn("gnome-screensaver-command --lock")),

    # Quit window
    Key([mod], "q", lazy.window.kill()),

    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, shift], "j", lazy.layout.shuffle_down()),
    Key([mod, shift], "k", lazy.layout.shuffle_up()),

    Key([mod], "h", lazy.screen.prevgroup()),
    Key([mod], "l", lazy.screen.nextgroup()),
    
    Key([mod], "m",    lazy.nextlayout()),

    Key([mod, "control"], "r", lazy.restart()),
]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, shift], i.name, lazy.window.togroup(i.name))
    )
