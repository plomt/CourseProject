import QtQuick  2.15
import QtQuick.Window 2.1
import QtQuick.Controls 2.15

ApplicationWindow {
    id: current_seance
    minimumWidth: 320
    minimumHeight: 240
    width:  500
    height: 480
    title: qsTr("Монитор консоли")
    TableView{
            id:tableView
            anchors.fill:parent
            model:seanceTable
            topMargin:horizontalHeader.implicitHeight
            delegate:Rectangle{
                implicitWidth:text.width + 24
                implicitHeight: text.height
                border.width: 1
                Text {
                        id:text
                        text: display
                        anchors.centerIn: parent
                 }
            }

     }
     HorizontalHeaderView {
            id: horizontalHeader
            syncView: tableView
            anchors.left: tableView.left
     }
     
    Component.onCompleted:{seanceTable.update(window.currentSeanceId)}
}
