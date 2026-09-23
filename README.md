# Omarchy Workspace Layout

A [dwm](https://dwm.suckless.org/)-style workspace layout indicator for the
Omarchy bar. It shows the focused workspace's [Hyprland layout](https://wiki.hypr.land/configuring/layouts/)
beside the workspace numbers. The symbol updates when you switch workspaces or
change layouts.

![The Omarchy bar on an empty workspace with the master layout selected](preview.png)

## Layout symbols

| Layout | Symbol |
| --- | --- |
| [Dwindle](https://wiki.hypr.land/configuring/layouts/dwindle-layout/) | `[\]` |
| [Master](https://wiki.hypr.land/configuring/layouts/master-layout/) | `[]=` |
| [Scrolling](https://wiki.hypr.land/configuring/layouts/scrolling-layout/) | `\|\|\|` |
| [Monocle](https://wiki.hypr.land/configuring/layouts/monocle-layout/) | `[M]` |

## Switching layouts

Hyprland includes all four layouts; no separate setup is needed. After
installing the plugin, click its symbol on a numbered workspace to cycle through
dwindle, master, scrolling, and monocle. The plugin saves the selected layout
for that workspace.

The indicator also follows layout changes made with `Super+L`. Named and
special workspaces show their layout but cannot be changed by clicking. Every
bar shows the focused workspace's layout.

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
