# Omarchy Workspace Layout

A [Dwm](https://dwm.suckless.org/) style layout indicator for the Omarchy bar.
It shows the [Hyprland layout](https://wiki.hypr.land/configuring/layouts/)
beside the workspace numbers.

![The Omarchy bar on an empty workspace with the master layout selected](preview.png)

## Layout symbols

| Layout | Symbol |
| --- | --- |
| [Dwindle](https://wiki.hypr.land/configuring/layouts/dwindle-layout/) | `[\]` |
| [Master](https://wiki.hypr.land/configuring/layouts/master-layout/) | `[]=` |
| [Scrolling](https://wiki.hypr.land/configuring/layouts/scrolling-layout/) | `\|\|\|` |
| [Monocle](https://wiki.hypr.land/configuring/layouts/monocle-layout/) | `[M]` |

## Switching layouts

Hyprland includes all four layouts. Click the symbol to cycle through the
enabled layouts. The symbol shows the active layout on each monitor.

## Settings

Open the widget settings in Omarchy's bar editor to choose the layouts in the
cycle. Dwindle, Master, Scrolling, and Monocle are all enabled by default. Keep
at least one enabled.

**Layout scope** controls where a selection applies:

| Scope | Behavior |
| --- | --- |
| Monitor (default) | One layout per monitor, shared by its workspaces. |
| Workspace | Each workspace keeps its own layout. |
| Global | One layout across all monitors and workspaces. |

If you disable the current layout, the next cycle selects the first enabled
one. Clicking the bar symbol and the optional `Super+L` binding use the same
settings.

## Installation

Install with Omarchy using SSH access to this private repository:

```bash
omarchy plugin add git@github.com:jesusarchive/omarchy-workspace-layout.git --enable
```

Choose the left bar section, then drag the widget after the workspace numbers.

## Cycle all layouts with Super+L

Omarchy's default shortcut cycles only dwindle and scrolling. To use the plugin's
layout selection and scope with `Super+L`, add this to
`~/.config/hypr/bindings.lua`:

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
