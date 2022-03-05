import QtQuick 2.6
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import Terminal 1.0
ApplicationWindow {
    id: window
    width: 1000
    height: 480
    title: "Terminal"
    visible: true
    minimumWidth: 320
    minimumHeight: 240

    MyTerm{
    id: term
    anchors.fill:parent
    color: "#212121"
    focus: true
    }



}
