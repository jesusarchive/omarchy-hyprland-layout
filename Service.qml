import QtQuick
import Quickshell.Hyprland
import Quickshell.Io

Item {
  id: root

  readonly property string helper: String(Qt.resolvedUrl("bin/hyprland-layout-cycle")).replace(/^file:\/\//, "")
  property bool pending: false

  function sync() {
    if (syncProcess.running) {
      pending = true
      return
    }
    syncProcess.running = true
  }

  Component.onCompleted: syncTimer.start()

  Connections {
    target: Hyprland
    function onRawEvent(event) {
      if (!event || !event.name) return
      var name = String(event.name)
      if (name === "workspace" || name === "workspacev2" ||
          name === "focusedmon" || name === "monitoradded" ||
          name === "monitorremoved" || name === "configreloaded") syncTimer.restart()
    }
  }

  Timer {
    id: syncTimer
    interval: 100
    onTriggered: root.sync()
  }

  Process {
    id: syncProcess
    command: [root.helper, "sync"]
    onRunningChanged: {
      if (!running && root.pending) {
        root.pending = false
        syncTimer.restart()
      }
    }
  }
}
