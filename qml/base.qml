import QtQuick 2.6
import QtQuick.Window 2.2
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.2
import Terminal 1.0

ApplicationWindow {
    id: window
    width: 1000
    height: 480
    title: qsTr("Terminal")
    visible: true
    minimumWidth: 320
    minimumHeight: 240

    Tabs {
        id: tabView
        anchors.fill:parent
        property Item activeTabItem
        Component {
            id: terminalScreenComponent
            MyTerm{
                id:terminal
                anchors.fill: parent
                focus:true
                color: "#212121"
            }
        }
        Component.onCompleted: {
            item_component = terminalScreenComponent
            createTab(terminalScreenComponent);

        }
    }
}
