# Omarchy Workspace Layout

[Dwm](https://dwm.suckless.org/) style layout indicator for the Omarchy bar.
It shows the current [Hyprland layout](https://wiki.hypr.land/configuring/layouts/)
beside the workspace numbers. Click the symbol to change layouts.

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
omarchy bar set jesusarchive.workspace-layout layoutScope monitor
omarchy bar set jesusarchive.workspace-layout enableDwindle true --json
omarchy bar set jesusarchive.workspace-layout enableMaster true --json
omarchy bar set jesusarchive.workspace-layout enableScrolling true --json
omarchy bar set jesusarchive.workspace-layout enableMonocle false --json
```

Set `layoutScope` to `monitor`, `workspace`, or `global`. Use `true --json` to
include a layout in the cycle and `false --json` to exclude it.

The bar click and the optional `Super+L` shortcut use these settings.

## Installation

Install from the private repository:

```bash
omarchy plugin add git@github.com:jesusarchive/omarchy-workspace-layout.git --enable
```

Choose the left bar section, then drag the widget after the workspace numbers.

## Super+L

Omarchy's default `Super+L` cycles dwindle and scrolling. To use this plugin's
layout list and scope, add this to `~/.config/hypr/bindings.lua`:

```lua
o.rebind(
  "SUPER + L",
  "Cycle workspace layout",
  os.getenv("HOME") .. "/.config/omarchy/plugins/jesusarchive.workspace-layout/bin/hyprland-workspace-layout-cycle"
)
```

## Removal

```bash
omarchy plugin remove jesusarchive.workspace-layout
```

Remove the `Super+L` override from `~/.config/hypr/bindings.lua` if you added it.

Licensed under [MIT](LICENSE).
