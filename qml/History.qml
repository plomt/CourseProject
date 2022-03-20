import QtQuick  2.15
import QtQuick.Window 2.1 // needed for the Window component
import QtQuick.Controls 2.14
Window {

    id: his_win
    minimumWidth: 320
    minimumHeight: 240
    width: 640
    height: 480
    title: qsTr("History")
    Row{
    anchors.fill: parent
        ScrollView{
            id:seances
            width: 100
            height: parent.height
        ListView{
            id:list
            anchors.fill:parent
            model: seanceModel
            highlight: Rectangle{y:deleg.y/2 + 100;width:deleg.width; height:15;color: "#8f9193";radius: 4 }
            delegate: Item{
                    id:deleg
                    width:parent.width
                    height: 20
                    property variant myData: pyLabel
                    Text {
                        text: "Seance " + pyLabel
                        anchors.centerIn:parent;
                        anchors.margins: 5;
                    }
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            showTable(pyLabel);
                        }
                        onEntered: {
                            list.currentIndex = index;
                        }
                    }
                    Rectangle {
                                id:bottom_line
                                color: "#999999"
                                width:parent.width
                                height: 1
                                anchors.bottom:parent.bottom
                  }
                  Rectangle {
                                id:vertical_line
                                color: "#999999"
                                width:1
                                height:  bottom_line.y - vertical_line.y
                                anchors.right: parent.right
                  }
                }
            }
        }
        spacing:10
        ScrollView{
        width: parent.width - seances.width
        height: parent.height
        clip:true
        TableView{
            id:table
            model:seanceTable
            anchors.fill:parent
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
        }
        Component.onCompleted:{
            table.model = []
        }
    }
    function showTable(str){

        var sp = str.split(' ')
        seanceTable.update(sp[0]);
        table.model = seanceTable;
    }
}
