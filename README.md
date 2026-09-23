# Omarchy Workspace Layout

A [dwm](https://dwm.suckless.org/)-style workspace layout indicator for the
Omarchy bar. It shows the focused workspace's [Hyprland layout](https://wiki.hypr.land/configuring/layouts/)
beside the workspace numbers. The symbol updates when you switch workspaces or
use Omarchy's `Super+L` shortcut.

![The Omarchy bar on an empty workspace with the master layout selected](preview.png)

## Layout symbols

| Layout | Symbol |
| --- | --- |
| [Dwindle](https://wiki.hypr.land/configuring/layouts/dwindle-layout/) | `[\]` |
| [Master](https://wiki.hypr.land/configuring/layouts/master-layout/) | `[]=` |
| [Scrolling](https://wiki.hypr.land/configuring/layouts/scrolling-layout/) | `\|\|\|` |
| [Monocle](https://wiki.hypr.land/configuring/layouts/monocle-layout/) | `[M]` |

Hyprland includes all four layouts. On a numbered workspace, click the symbol
to cycle through them. The selected layout is saved for that workspace. Named
and special workspaces show their layout but cannot be changed by clicking.
Every bar shows the focused workspace's layout.

## Installation

Install with Omarchy using SSH access to this private repository:

```bash
omarchy plugin add git@github.com:jesusarchive/omarchy-workspace-layout.git --enable
```

Choose the left bar section, then drag the widget after the workspace numbers.

## Removal

```bash
omarchy plugin remove jesusarchive.workspace-layout
```

Licensed under [MIT](LICENSE).
