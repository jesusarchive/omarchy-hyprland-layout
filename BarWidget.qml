import QtQuick
import Quickshell
import Quickshell.Hyprland
import Quickshell.Io
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "jesusarchive.workspace-layout"

  property string layoutName: ""
  property int workspaceId: 0
  property bool refreshPending: false

  readonly property string symbol: {
    switch (layoutName) {
    case "dwindle": return "[\\]"
    case "master": return "[]="
    case "scrolling": return "|||"
    case "monocle": return "[M]"
    default: return "[?]"
    }
  }

  function refresh() {
    if (query.running) {
      refreshPending = true
      return
    }
    refreshPending = false
    query.running = true
  }

  Component.onCompleted: refresh()

  // Workspace switches have compositor events. A short poll also catches
  // layout changes made through Hyprland's workspace rule command.
  Connections {
    target: Hyprland
    function onRawEvent(event) {
      if (!event || !event.name) return
      var name = String(event.name)
      if (name === "workspace" || name === "workspacev2" ||
          name === "focusedmon" || name === "configreloaded") root.refresh()
    }
  }

  Timer {
    interval: 1500
    running: root.visible
    repeat: true
    onTriggered: root.refresh()
  }

  Process {
    id: query
    command: ["hyprctl", "-j", "activeworkspace"]
    onRunningChanged: {
      if (!running && root.refreshPending) root.refresh()
    }
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        try {
          var workspace = JSON.parse(text || "{}")
          root.workspaceId = Number(workspace.id) || 0
          root.layoutName = String(workspace.tiledLayout || "")
        } catch (e) {
          root.layoutName = ""
        }
      }
    }
  }

  // Super+L writes the per-workspace rule before applying it. Watch that file
  // and query once Hyprland has had a moment to apply the new layout.
  FileView {
    path: root.workspaceId > 0
      ? (Quickshell.env("HOME") || "") + "/.local/state/omarchy/workspace-layouts/" + root.workspaceId + ".lua"
      : ""
    watchChanges: true
    printErrors: false
    onFileChanged: shortcutRefresh.restart()
  }

  Timer {
    id: shortcutRefresh
    interval: 150
    onTriggered: root.refresh()
  }

  implicitWidth: root.vertical ? root.barSize : label.implicitWidth + 14
  implicitHeight: root.vertical ? label.implicitWidth + 14 : root.barSize

  Text {
    id: label
    anchors.centerIn: parent
    text: root.symbol
    color: root.bar ? root.bar.barForeground : Color.foreground
    opacity: 0.85
    font.family: "monospace"
    font.pixelSize: Style.font.body
    textFormat: Text.PlainText
    rotation: root.vertical ? -90 : 0
  }

  MouseArea {
    anchors.fill: parent
    hoverEnabled: true
    acceptedButtons: Qt.LeftButton
    cursorShape: Qt.PointingHandCursor
    onClicked: {
      var helper = String(Qt.resolvedUrl("bin/hyprland-workspace-layout-cycle")).replace(/^file:\/\//, "")
      if (root.bar) root.bar.run(Util.shellQuote(helper))
      Qt.callLater(root.refresh)
    }
    onEntered: if (root.bar) root.bar.showTooltip(root, root.layoutName || "Unknown layout")
    onExited: if (root.bar) root.bar.hideTooltip(root)
  }
}
