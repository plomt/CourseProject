import QtQuick  2.15
import QtQuick.Window 2.1
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: current_seance
    minimumWidth: 320
    minimumHeight: 240
    width:  640
    height: 500
    title: qsTr("Монитор консоли")
    TableView{
            id:tableView
            width:parent.width
            height:400
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

     property string back_color: "#212121"
     property string text_color:  "white"
     Row{
        anchors.top:tableView.bottom
        anchors.topMargin: 50
        spacing: 20
        Button {
            id:back
            text: "Цвет текста"
            onClicked: {textColorDialog.visible = true}
        }
        Rectangle{
            width:back.width / 2
            height: back.height
            border.width:1
            border.color: "black"
            color: text_color
        }
        Button {
            text: "Применить"
            onClicked: {tabCreator.changeColors(text_color)}
        }
        Button{
        text: "Обновить"
        onClicked: {seanceTable.update(window.currentSeanceId)}
        }
    }

    Component.onCompleted:{seanceTable.update(window.currentSeanceId)}

    ColorDialog {
    id: colorDialog
    title: "Please choose a background color"
    onAccepted: {
        //console.log("You chose: " + colorDialog.color)
        back_color = colorDialog.color
    }

    }
     ColorDialog {
    id: textColorDialog
    title: "Please choose a text color"
    onAccepted: {
        //console.log("You chose: " + textColorDialog.color)
        text_color = textColorDialog.color
    }

    }
}
