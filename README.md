# Omarchy Workspace Layout

Show the current Hyprland workspace layout beside the workspace numbers in
the Omarchy bar. The compact symbol follows workspace switches and changes made
with `Super+L`. Click the symbol to cycle layouts.

![Omarchy bar showing the dwindle symbol on an empty workspace](preview.png)

The screenshot shows an empty workspace. The layout symbol is the `[\]` mark
just after the workspace numbers. A closer view of that part of the bar:

![Workspace numbers followed by the layout symbol](assets/bar-detail.png)

## Layout symbols

| Hyprland layout | Symbol | Source |
| --- | --- | --- |
| Dwindle | `[\]` | [dwm Fibonacci patch](https://dwm.suckless.org/patches/fibonacci/) |
| Master | `[]=` | [dwm tile layout](https://git.suckless.org/dwm/file/config.def.h.html) |
| Scrolling | `|||` | This plugin's shorthand for scrolling columns |
| Monocle | `[M]` | [dwm monocle layout](https://git.suckless.org/dwm/file/config.def.h.html) |

Hyprland reports these layout names through `hyprctl -j activeworkspace`. It
does not assign bar symbols. [xmonad's status bar API](https://xmonad.github.io/xmonad-docs/xmonad-contrib/src/XMonad.Hooks.StatusBar.PP.html)
reports a layout name and lets the user format it.

## Install

This repository has a root `manifest.json`, so Omarchy can install it as a
plugin from a Git repository:

```bash
omarchy plugin add <repository-url> --enable
```

Choose the left bar section when prompted. You can drag the widget after the
workspace numbers. Clicking the widget works after installation because the
layout cycle command is included in this repository.

For a local checkout, run:

```bash
./install.sh
```

The local installer validates the plugin, copies it to
`~/.config/omarchy/plugins/jesusarchive.workspace-layout`, installs the cycle
command in `~/.local/bin`, and places the widget after `omarchy.workspaces` in
`~/.config/omarchy/shell.json`. It backs up `shell.json` before changing it.
Running it again updates the copied files without adding another bar entry.

## Keyboard shortcut

The included cycle command visits `dwindle`, `master`, `scrolling`, and
`monocle` in that order. To make `Super+L` run it, put this in
`~/.config/hypr/bindings.lua`:

```lua
o.rebind("SUPER + L", "Cycle workspace layout", os.getenv("HOME") .. "/.config/omarchy/plugins/jesusarchive.workspace-layout/bin/hyprland-workspace-layout-cycle")
```

`o.rebind` replaces Omarchy's default `Super+L` binding, which toggles only
dwindle and scrolling. The command writes Omarchy's per-workspace layout rule,
so the choice survives a Hyprland reload. The widget watches that file for
shortcut changes and checks Hyprland every 1.5 seconds for changes made by
other commands.

## Remove

```bash
omarchy plugin remove jesusarchive.workspace-layout
```

If you added the `Super+L` binding above, remove that line to restore Omarchy's
default shortcut. A local install also leaves the copied command in
`~/.local/bin/hyprland-workspace-layout-cycle`; remove it if nothing else uses
it.

## Requirements and limits

- Omarchy with its Quickshell bar, `hyprctl`, and `jq`. Tested with Hyprland 0.56.2.
- The symbol describes the focused workspace. With multiple monitors, every
  bar currently shows that same focused workspace layout.
- The included cycle command targets numbered workspaces. Named and special
  workspaces still show their reported layout, but the click and shortcut
  command do not set a new layout there.

The plugin code is MIT licensed. See [LICENSE](LICENSE).
