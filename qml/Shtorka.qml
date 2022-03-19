import QtQuick 2.6



Rectangle {
    id:comboBox
    property variant items: ["Сеансы", "Параметры"]
    property alias selectedIndex: listView.currentIndex;
    signal comboClicked(var str);
    z: 100;
    smooth:true;

    Rectangle {
        id:dropDown
        width:100;
        height:0;
        clip:true;
        radius:4;
        anchors.top: parent.top;
        anchors.margins: 2;
        color: "lightgray"

        ListView {
            id:listView
            height:500;
            model: comboBox.items
            highlight:highlightor
            delegate: Item{
                width:dropDown.width;
                height: 30;
                property variant myData: modelData
                Text {
                    text: modelData
                    anchors.top: parent.top;
                    anchors.left: parent.left;
                    anchors.margins: 5;

                }
                MouseArea {
                    anchors.fill: parent;
                    hoverEnabled: true
                    onClicked: {
                        comboBox.state = ""
                        comboBox.comboClicked(listView.currentItem.myData);
                    }
                    onEntered: {
                        listView.currentIndex = index;
                    }
                }
            }
        }
    }

    Component {
        id: highlightor
        Rectangle {
            width:comboBox.width;
            height:comboBox.height;
            color: "#8f9193";
            radius: 4
        }
    }

    states: State {
        name: "dropDown";
        PropertyChanges { target: dropDown; height:40*comboBox.items.length }
    }

    transitions: Transition {
        NumberAnimation { target: dropDown; properties: "height"; easing.type: Easing.OutExpo; duration: 1000 }
    }
    Component.onCompleted: {comboClicked.connect(show_window)}

    function show_window(str){
        if (str === "Сеансы"){
            var component = Qt.createComponent("History.qml")
            var window    = component.createObject(null)
            window.show()
        }
    }

}
