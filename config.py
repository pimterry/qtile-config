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

startup_apps = [
    lambda: sh.xsetroot('-cursor_name', 'left_ptr', '-solid', '#000000'),
    ensure_running("gnome-keyring-daemon", lambda: sh.gnome_session(_bg=True)),
    ensure_running("nm-applet", lambda: sh.nm_applet(_bg=True)),
    lambda: sh.seafile("start", _bg=True),
    lambda: sh.emoji_keyboard(_bg=True)
]

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
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8")
]

dgroups_key_binder = None
dgroups_app_rules = []

layouts = [
    layout.MonadTall(border_width=1, border_focus="#dddddd"),
    layout.Max()
]

screens = [Screen(top=bar.Bar([
                      widget.GroupBox(fontsize=12, borderwidth=2),
                      widget.Sep(),
                      widget.TaskList(fontsize=12, padding=4, borderwidth=2),
                      widget.Sep(),
                      widget.Prompt(),
                      widget.Notify(),
                      widget.Systray(),
                      widget.Volume(fontsize=12),
                      widget.Battery(battery_name='BAT0',
                                     energy_now_file='charge_now',
                                     energy_full_file='charge_full',
                                     power_now_file='current_now',
                                     update_delay=1,
                                     charge_char=u"↑",
                                     discharge_char=u"↓",
                                     format='{char} {percent:2.0%}',
                                     fontsize=12),
                      widget.Clock(format='%Y-%m-%d %a %I:%M %p',
                                   fontsize=12),
                  ], 22)),
            Screen()]

mod = "mod4"
alt = "mod1"
control = "control"
shift = "shift"

keys = [
    # Log out
    Key([mod, control], "Escape", lazy.shutdown()),

    # Device shortcuts
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -q set Master 3dB+")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("amixer -q set Master 3dB-")),
    Key([], "XF86AudioMute",
        lazy.spawn("amixer -D pulse set Master toggle")),

    Key([], "XF86MonBrightnessUp", lazy.spawn("acpilight -inc 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("acpilight -dec 10")),

    # Run shortcuts
    Key([mod], "t", lazy.spawn("gnome-terminal")),
    Key([mod], "e", lazy.spawn("thunar")),
    Key([mod], "c", lazy.spawn("google-chrome")),
    Key([mod], "v", lazy.spawn("gvim")),
    Key([mod], "r", lazy.spawn("dmenu_run -fn 'Fira Code' -p '>'")),
    Key([control, mod, alt], "l", lazy.spawn("gnome-screensaver-command --lock")),

    # Quit window
    Key([mod], "q", lazy.window.kill()),

    # Move windows around
    Key([alt], "Tab", lazy.layout.down()),
    Key([alt, shift], "Tab", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, shift], "j", lazy.layout.shuffle_down()),
    Key([mod, shift], "k", lazy.layout.shuffle_up()),
    Key([control, mod], "n", lazy.layout.normalize()),
    Key([control, mod], "k", lazy.layout.grow()),
    Key([control, mod], "j", lazy.layout.shrink()),

    # Manage workspaces
    Key([mod], "Tab", lazy.screen.next_group()),
    Key([mod, shift], "Tab", lazy.screen.prev_group()),
    Key([mod], "l", lazy.screen.next_group()),
    Key([mod], "h", lazy.screen.prev_group()),
    Key([mod], "m", lazy.next_layout()),

    # Multimedia keys
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause')),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous')),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next')),

    Key([], "Print", lazy.spawn('gnome-screenshot')),
    Key([control], "Print", lazy.spawn('gnome-screenshot -a')),

    Key([control, mod], "space", lazy.spawn('emoji-keyboard -s')),

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
