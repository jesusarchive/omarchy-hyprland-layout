# Omarchy Hyprland Layout

[Dwm](https://dwm.suckless.org/) style layout indicator for the Omarchy bar.
It shows the current [Hyprland layout](https://wiki.hypr.land/configuring/layouts/).
Click the symbol to change layouts.

![The Omarchy bar on an empty workspace with the master layout selected](preview.png)

## Layout symbols

| Layout | Symbol |
| --- | --- |
| [Dwindle](https://wiki.hypr.land/configuring/layouts/dwindle-layout/) | `[\]` |
| [Master](https://wiki.hypr.land/configuring/layouts/master-layout/) | `[]=` |
| [Scrolling](https://wiki.hypr.land/configuring/layouts/scrolling-layout/) | `\|\|\|` |
| [Monocle](https://wiki.hypr.land/configuring/layouts/monocle-layout/) | `[M]` |

## Plugin properties

The bar editor lets you choose which layouts to cycle through. All four are
enabled by default. Keep at least one enabled.

The scope controls where the selected layout applies:

| Scope | Behavior |
| --- | --- |
| monitor (default) | One layout per monitor, shared by its workspaces. |
| workspace | Each workspace keeps its own layout. |
| global | One layout across all monitors and workspaces. |

You can set the same properties from a terminal:

```bash
omarchy bar set jesusarchive.hyprland-layout layoutScope monitor
omarchy bar set jesusarchive.hyprland-layout enableDwindle true --json
omarchy bar set jesusarchive.hyprland-layout enableMaster true --json
omarchy bar set jesusarchive.hyprland-layout enableScrolling true --json
omarchy bar set jesusarchive.hyprland-layout enableMonocle false --json
```

Set `layoutScope` to `monitor`, `workspace`, or `global`. Use `true --json` to
include a layout in the cycle and `false --json` to exclude it.

The bar click and the optional `Super+L` shortcut use these settings.

## Installation

Install from GitHub:

```bash
omarchy plugin add https://github.com/jesusarchive/omarchy-hyprland-layout.git --enable
```

Place the widget in the left bar section.

The helper requires Python 3 and `hyprctl`.

## Super+L

Omarchy's default `Super+L` cycles dwindle and scrolling. To use this plugin's
layout list and scope, add this to `~/.config/hypr/bindings.lua`:

```lua
o.rebind(
  "SUPER + L",
  "Cycle Hyprland layout",
  os.getenv("HOME") .. "/.config/omarchy/plugins/jesusarchive.hyprland-layout/bin/hyprland-layout-cycle"
)
```

## Removal

```bash
omarchy plugin remove jesusarchive.hyprland-layout
```

Remove the `Super+L` override from `~/.config/hypr/bindings.lua` if you added it.
To discard the saved scope and layouts, remove
`~/.local/state/omarchy-hyprland-layout/`. Omarchy keeps the workspace layout
rules the plugin wrote in `~/.local/state/omarchy/workspace-layouts/`.

Licensed under [MIT](LICENSE).
