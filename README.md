# Omarchy Workspace Layout

A [dwm](https://dwm.suckless.org/)-style workspace layout indicator for the
Omarchy bar. It shows the focused Hyprland workspace's layout beside the
workspace numbers and updates when you switch workspaces or use Omarchy's
`Super+L` shortcut. Click the symbol to cycle layouts.

![The Omarchy bar on an empty workspace with the master layout selected](preview.png)

## Layout symbols

| Layout | Symbol |
| --- | --- |
| Dwindle | `[\]` |
| Master | `[]=` |
| Scrolling | `\|\|\|` |
| Monocle | `[M]` |

These are Hyprland's four built-in layouts. Every bar shows the focused
workspace's layout. Clicking cycles layouts on numbered workspaces only.

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
