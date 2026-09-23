# Omarchy Workspace Layout

Show the current Hyprland workspace layout as a dwm-style symbol beside the
workspace numbers in the Omarchy bar. The symbol updates when you switch
workspaces or press `Super+L`. Click it to cycle layouts. It currently supports
Hyprland's four built-in layouts: dwindle, master, scrolling, and monocle.

![The Omarchy bar on an empty workspace with the master layout selected](preview.png)

## Symbols

| Layout | Symbol |
| --- | --- |
| Dwindle | `[\]` |
| Master | `[]=` |
| Scrolling | `\|\|\|` |
| Monocle | `[M]` |

## Installation

Install with Omarchy:

```bash
omarchy plugin add git@github.com:jesusarchive/omarchy-workspace-layout.git --enable
```

Choose the left bar section, then drag the widget after the workspace numbers.

## Shortcut

The included command cycles dwindle, master, scrolling, and monocle. To bind it
to `Super+L`, add this to `~/.config/hypr/bindings.lua`:

```lua
o.rebind("SUPER + L", "Cycle workspace layout", os.getenv("HOME") .. "/.config/omarchy/plugins/jesusarchive.workspace-layout/bin/hyprland-workspace-layout-cycle")
```

This replaces Omarchy's default `Super+L` action, which cycles only dwindle
and scrolling.

## Removal

```bash
omarchy plugin remove jesusarchive.workspace-layout
```

Remove the shortcut line if you added it.

The widget shows the focused workspace's layout on every monitor. The cycle
command works on numbered workspaces; named and special workspaces are
display-only.

The code uses the [MIT License](LICENSE).
