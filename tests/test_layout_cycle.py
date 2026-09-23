import importlib.machinery
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "bin/hyprland-layout-cycle"
loader = importlib.machinery.SourceFileLoader("layout_cycle", str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
layout_cycle = importlib.util.module_from_spec(spec)
loader.exec_module(layout_cycle)


class LayoutCycleTests(unittest.TestCase):
    def setUp(self):
        self.workspaces = [
            {"id": 1, "monitor": "DP-1", "tiledLayout": "dwindle"},
            {"id": 2, "monitor": "DP-1", "tiledLayout": "dwindle"},
            {"id": 3, "monitor": "HDMI-A-1", "tiledLayout": "dwindle"},
        ]
        self.monitors = [
            {"monitor": "DP-1", "workspace": 1, "layout": "dwindle"},
            {"monitor": "HDMI-A-1", "workspace": 3, "layout": "dwindle"},
        ]

    def cycle(self, scope, state=None, settings=None):
        state = {} if state is None else state
        settings = {"layoutScope": scope, **(settings or {})}
        with patch.object(layout_cycle, "widget_settings", return_value=settings), \
             patch.object(layout_cycle, "workspaces_on_monitors", return_value=self.monitors), \
             patch.object(layout_cycle, "numbered_workspaces", return_value=self.workspaces), \
             patch.object(layout_cycle, "apply_layout") as apply, \
             patch.object(layout_cycle, "save_state") as save, \
             patch.object(layout_cycle.subprocess, "run"):
            layout_cycle.cycle(state, "DP-1")
        save.assert_called_once_with(state)
        return state, apply.call_args_list

    def test_monitor_scope_changes_only_that_monitors_workspaces(self):
        state, calls = self.cycle("monitor")
        self.assertEqual(state, {"_scope": "monitor", "DP-1": "master"})
        self.assertEqual([call.args for call in calls], [(1, "master"), (2, "master")])

    def test_global_scope_changes_all_monitors(self):
        state, calls = self.cycle("global")
        self.assertEqual(state, {"_scope": "global", "_layout": "master"})
        self.assertEqual([call.args for call in calls], [(1, "master"), (2, "master"), (3, "master")])

    def test_workspace_scope_changes_only_current_workspace(self):
        state, calls = self.cycle("workspace")
        self.assertEqual(state, {"_scope": "workspace"})
        self.assertEqual([call.args for call in calls], [(1, "master")])

    def test_disabled_layouts_are_skipped(self):
        state, calls = self.cycle("workspace", settings={"enableMaster": False})
        self.assertEqual(state["_scope"], "workspace")
        self.assertEqual([call.args for call in calls], [(1, "scrolling")])


if __name__ == "__main__":
    unittest.main()
