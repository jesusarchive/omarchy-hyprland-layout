import importlib.machinery
import importlib.util
import tempfile
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
        self.assertEqual(state, {"_scope": "monitor", "DP-1": "scrolling"})
        self.assertEqual([call.args for call in calls], [(1, "scrolling"), (2, "scrolling")])

    def test_global_scope_changes_all_monitors(self):
        state, calls = self.cycle("global")
        self.assertEqual(state, {"_scope": "global", "_layout": "scrolling"})
        self.assertEqual([call.args for call in calls], [(1, "scrolling"), (2, "scrolling"), (3, "scrolling")])

    def test_workspace_scope_changes_only_current_workspace(self):
        state, calls = self.cycle("workspace")
        self.assertEqual(state, {"_scope": "workspace"})
        self.assertEqual([call.args for call in calls], [(1, "scrolling")])

    def test_disabled_layouts_are_skipped(self):
        state, calls = self.cycle("workspace", settings={"enableScrolling": False})
        self.assertEqual(state["_scope"], "workspace")
        self.assertEqual([call.args for call in calls], [(1, "master")])


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.rules = tempfile.TemporaryDirectory()
        self.addCleanup(self.rules.cleanup)
        self.rules_dir = Path(self.rules.name)
        self.workspaces = [
            {"id": 1, "monitor": "DP-1", "tiledLayout": "dwindle"},
            {"id": 2, "monitor": "DP-1", "tiledLayout": "master"},
            {"id": 3, "monitor": "HDMI-A-1", "tiledLayout": "dwindle"},
        ]
        self.monitors = [
            {"monitor": "DP-1", "workspace": 1, "layout": "dwindle"},
            {"monitor": "HDMI-A-1", "workspace": 3, "layout": "dwindle"},
        ]

    def write_rule(self, workspace_id, layout):
        (self.rules_dir / f"{workspace_id}.lua").write_text(layout_cycle.rule_text(workspace_id, layout))

    def sync(self, scope, state, settings=None, active_layout="dwindle"):
        settings = {"layoutScope": scope, **(settings or {})}
        with patch.object(layout_cycle, "RULES_DIR", self.rules_dir), \
             patch.object(layout_cycle, "widget_settings", return_value=settings), \
             patch.object(layout_cycle, "workspaces_on_monitors", return_value=self.monitors), \
             patch.object(layout_cycle, "numbered_workspaces", return_value=self.workspaces), \
             patch.object(layout_cycle, "hyprctl_json", return_value={"tiledLayout": active_layout}), \
             patch.object(layout_cycle, "apply_layout") as apply, \
             patch.object(layout_cycle, "save_state") as save:
            layout_cycle.sync(state)
        return [call.args for call in apply.call_args_list], save.called

    def test_workspace_scope_only_records_scope(self):
        state = {"_scope": "monitor", "DP-1": "master"}
        calls, saved = self.sync("workspace", state)
        self.assertEqual(state, {"_scope": "workspace"})
        self.assertEqual(calls, [])
        self.assertTrue(saved)

    def test_workspace_scope_unchanged_does_not_save(self):
        calls, saved = self.sync("workspace", {"_scope": "workspace"})
        self.assertEqual(calls, [])
        self.assertFalse(saved)

    def test_monitor_scope_adopts_current_layouts(self):
        state = {}
        calls, saved = self.sync("monitor", state)
        self.assertEqual(state, {"_scope": "monitor", "DP-1": "dwindle", "HDMI-A-1": "dwindle"})
        self.assertEqual(calls, [(1, "dwindle"), (3, "dwindle")])
        self.assertTrue(saved)

    def test_monitor_scope_restores_drifted_workspace(self):
        self.write_rule(1, "master")
        self.write_rule(3, "dwindle")
        state = {"_scope": "monitor", "DP-1": "master", "HDMI-A-1": "dwindle"}
        calls, saved = self.sync("monitor", state)
        self.assertEqual(calls, [(1, "master")])
        self.assertFalse(saved)

    def test_monitor_scope_replaces_disabled_layout(self):
        self.write_rule(1, "dwindle")
        self.write_rule(3, "dwindle")
        state = {"_scope": "monitor", "DP-1": "master", "HDMI-A-1": "dwindle"}
        calls, saved = self.sync("monitor", state, settings={"enableMaster": False})
        self.assertEqual(state["DP-1"], "dwindle")
        self.assertEqual(calls, [])
        self.assertTrue(saved)

    def test_global_scope_adopts_active_layout(self):
        state = {}
        calls, saved = self.sync("global", state, active_layout="scrolling")
        self.assertEqual(state, {"_scope": "global", "_layout": "scrolling"})
        self.assertEqual(calls, [(1, "scrolling"), (2, "scrolling"), (3, "scrolling")])
        self.assertTrue(saved)

    def test_global_scope_falls_back_to_first_enabled(self):
        state = {}
        self.sync("global", state, settings={"enableDwindle": False}, active_layout="dwindle")
        self.assertEqual(state["_layout"], "scrolling")

    def test_global_scope_repairs_only_mismatches(self):
        for workspace_id in (1, 2, 3):
            self.write_rule(workspace_id, "dwindle")
        calls, saved = self.sync("global", {"_scope": "global", "_layout": "dwindle"})
        self.assertEqual(calls, [(2, "dwindle")])
        self.assertFalse(saved)

    def test_no_enabled_layouts_applies_nothing(self):
        disabled = {"enable" + layout.title(): False for layout in layout_cycle.LAYOUTS}
        for scope in ("monitor", "global"):
            with self.subTest(scope=scope):
                calls, _ = self.sync(scope, {"_scope": scope}, settings=disabled)
                self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
