import QtQuick  2.15
import QtQuick.Window 2.1
import QtQuick.Controls 2.14

ApplicationWindow {
    id: his_win
    minimumWidth: 320
    minimumHeight: 240
    width: 800
    height: 480
    title: qsTr("История сеансов")
    header:ToolBar{
        id: tools
        width:140
        ToolButton {
            text: qsTr("+")
            anchors.centerIn:parent
            onClicked: {tabCreator.newSeance();}
         }
    }
    Row{
    id: rows
    anchors.fill:parent
    width:parent.width
    anchors.bottom: parent.bottom
    anchors.top:tools.bottom
    ScrollView{
            id:seances
            width: 140
            height: parent.height
        ListView{
            id:list
            anchors.fill:parent
            model: seanceModel
            highlight: Rectangle{ height:15;color: "#8f9193";radius: 4 }
            delegate: Item{
                    id:deleg
                    width:seances.width
                    height: 20
                    property variant myData: pyLabel
                    Text {
                        text: "Seance " + pyLabel
                        anchors.centerIn:parent;
                        anchors.margins: 5;
                    }
                    MouseArea {
                        width: parent.width - 30
                        height:parent.height
                        anchors.left:parent.left
                        hoverEnabled: true
                        onClicked: {
                            showTable(pyLabel);
                            tabCreator.switchTab(pyLabel.split(' ')[0]);
                        }
                        onEntered: {
                            list.currentIndex = index;
                        }
                    }
                    Rectangle {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.rightMargin: 4
                    implicitWidth: 14
                    implicitHeight: 14
                    radius: width/2
                    color: control.hovered ? "#eee": "#ccc"
                    border.color: "gray"
                    Text {text: "X" ; anchors.centerIn: parent ; color: "gray"}
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            deleteSeance(pyLabel);
                        }
                        onEntered: {
                            list.currentIndex = index;
                        }
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
        id:view
        width: parent.width - seances.width
        height: rows.height
        clip:true
        property string currentId:""
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
        view.currentId = sp[0]
    }
    function deleteSeance(str){

        var SeanceId = str.split(' ')[0];
        seanceModel.delete(str);
        if (SeanceId == view.currentId)
            seanceTable.clearTable()
    }
    Connections{
        target:tabCreator
        function onNewWin() {
                 var component = Qt.createComponent("base.qml")
                 var window    = component.createObject(null)
                 tabCreator.changeState("True")
                 seanceModel.update("complete")
                 window.show()

            }
    }
}
