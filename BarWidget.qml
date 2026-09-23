import QtQuick
import Quickshell
import Quickshell.Hyprland
import Quickshell.Io
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "jesusarchive.hyprland-layout"

  property string layoutName: ""
  property bool refreshPending: false
  readonly property string helper: String(Qt.resolvedUrl("bin/hyprland-layout-cycle")).replace(/^file:\/\//, "")
  readonly property string monitorName: {
    var win = root.QsWindow.window
    return win && win.screen ? String(win.screen.name) : ""
  }

  onMonitorNameChanged: refresh()

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

  Connections {
    target: Hyprland
    function onRawEvent(event) {
      if (!event || !event.name) return
      var name = String(event.name)
      if (name === "workspace" || name === "workspacev2" ||
          name === "focusedmon" || name === "configreloaded") shortcutRefresh.restart()
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
    command: [root.helper, "status"]
    onRunningChanged: {
      if (!running && root.refreshPending) root.refresh()
    }
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        try {
          var monitors = JSON.parse(text || "[]")
          var current = monitors.find(function(item) { return item.monitor === root.monitorName })
          root.layoutName = current ? String(current.layout || "") : ""
        } catch (e) {
          root.layoutName = ""
        }
      }
    }
  }

  FileView {
    path: (Quickshell.env("HOME") || "") + "/.local/state/omarchy-hyprland-layout/state.json"
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
    enabled: root.layoutName !== "" && root.monitorName !== ""
    hoverEnabled: true
    acceptedButtons: Qt.LeftButton
    cursorShape: Qt.PointingHandCursor
    onClicked: {
      if (root.bar && root.monitorName)
        root.bar.run(Util.shellQuote(root.helper) + " cycle " + Util.shellQuote(root.monitorName))
    }
    onEntered: if (root.bar) root.bar.showTooltip(root, root.layoutName || "Unknown layout")
    onExited: if (root.bar) root.bar.hideTooltip(root)
  }
}
