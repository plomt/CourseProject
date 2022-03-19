import QtQuick 2.6
import QtQuick.Window 2.1 // needed for the Window component
import QtQuick.Controls 1.0
Window {

    id: his_win
    width: 640
    height: 480
    title: qsTr("History")
    function update(data){
        console.log("gey");
    }
    Row{
    anchors.fill: parent
    Column{
        id: seances
        width: parent.width / 8
        height: parent.height
        ScrollView{
            anchors.fill: parent
        ListView{
            id:list
            anchors.fill:parent
            model: ["seance1", "seance2"]
            delegate: Item{
                    id:deleg
                    width:parent.width
                    height: 15
                    property variant myData: modelData
                    Text {
                        text: modelData
                        anchors.top: parent.top;
                        anchors.left: parent.left;
                        anchors.margins: 5;
                 }
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            console.log(deleg.width)
                        }
                        onEntered: {
                        }
                    }
                    Rectangle {
                                color: "#999999"
                                width:parent.width
                                height: 1
                                anchors.top:parent.bottom
                                anchors.margins: 5
                                visible: (index !== (list.count - 1))
                  }
                }
            }
        }
       }
    }
}
