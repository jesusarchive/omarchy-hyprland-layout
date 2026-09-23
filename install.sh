#!/bin/bash
set -euo pipefail

repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
plugin_dir="$HOME/.config/omarchy/plugins/jesusarchive.workspace-layout"
shell_config="$HOME/.config/omarchy/shell.json"

omarchy plugin validate "$repo_dir"
mkdir -p "$plugin_dir/bin" "$HOME/.local/bin"
install -m 644 "$repo_dir/manifest.json" "$plugin_dir/manifest.json"
install -m 644 "$repo_dir/BarWidget.qml" "$plugin_dir/BarWidget.qml"
install -m 644 "$repo_dir/preview.png" "$plugin_dir/preview.png"
install -m 644 "$repo_dir/LICENSE" "$plugin_dir/LICENSE"
install -m 755 "$repo_dir/bin/hyprland-workspace-layout-cycle" "$plugin_dir/bin/hyprland-workspace-layout-cycle"
install -m 755 "$repo_dir/bin/hyprland-workspace-layout-cycle" "$HOME/.local/bin/hyprland-workspace-layout-cycle"

python3 - "$shell_config" <<'PY'
import json
import os
from datetime import datetime
from pathlib import Path
from shutil import copy2
from sys import argv

path = Path(argv[1])
config = json.loads(path.read_text())
left = config['bar']['layout']['left']
plugin_id = 'jesusarchive.workspace-layout'
old_id = 'jesusarchive.layout-viewer'

if any(item.get('id') == plugin_id for item in left):
    raise SystemExit(0)

backup = path.with_name(f'{path.name}.bak.workspace-layout-{datetime.now():%Y%m%d-%H%M%S}')
copy2(path, backup)
old_index = next((i for i, item in enumerate(left) if item.get('id') == old_id), None)
if old_index is not None:
    left[old_index] = {'id': plugin_id}
else:
    workspace_index = next((i for i, item in enumerate(left) if item.get('id') == 'omarchy.workspaces'), -1)
    left.insert(workspace_index + 1, {'id': plugin_id})

temporary = path.with_name(path.name + '.workspace-layout.tmp')
temporary.write_text(json.dumps(config, indent=2, ensure_ascii=False) + '\n')
os.chmod(temporary, path.stat().st_mode)
os.replace(temporary, path)
print(f'Updated {path}; backup: {backup}')
PY

omarchy-shell -q shell rescanPlugins
echo "Omarchy Workspace Layout installed"
