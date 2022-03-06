import QtQuick 2.6
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

TabView {
    id: tabView


    property Item activeTabItem
    onCurrentIndexChanged: {
           fixupVisibility()
       }
    function fixupVisibility() {
          var child = tabView.getTab(currentIndex)
          activeTabItem = child
          child.forceActiveFocus()
    }
    function _updateTabTitle() {
            for (var i = 0; i < tabView.count; ++i) {
                var obj = tabView.getTab(i).item
                if (obj === this) {
                    obj.title = this.title
                    return
                }
            }
    }
    function createTab(comp){
        if (comp.status != Component.Ready)
            return
        tabView.addTab("", terminalScreenComponent);
        tabView.currentIndex = tabView.count - 1;
        var tab = tabView.getTab(tabView.currentIndex)
        var title = tab.item.title ? tab.item.title : "Shell " + tabView.count
        tab.item.titleChanged.connect(_updateTabTitle.bind(tab.item))
        tab.title = title

        fixupVisibility()
    }


    style: TabViewStyle {
            property color frameColor: "#999"
            property color fillColor: "#eee"
            frameOverlap: 1
            frame: Rectangle {
                color: "#eee"
                border.color: frameColor
            }
            tab: Rectangle {
                color: styleData.selected ? fillColor : frameColor
                implicitWidth: Math.max(text.width + 24, 80)
                implicitHeight: 20
                Rectangle { height: 1 ; width: parent.width ; color: frameColor}
                Rectangle { height: parent.height ; width: 1; color: frameColor}
                Rectangle { x: parent.width -1; height: parent.height ; width: 1; color: frameColor}
                Text {
                    id: text
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.leftMargin: 6
                    text: styleData.title
                    color: styleData.selected ? "black" : "white"
                }
                Rectangle {
                    visible: tabView.count > 1
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.rightMargin: 4
                    implicitWidth: 16
                    implicitHeight: 16
                    radius: width/2
                    color: control.hovered ? "#eee": "#ccc"
                    border.color: "gray"
                    Text {text: "X" ; anchors.centerIn: parent ; color: "gray"}
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (tabView.count > 1)
                                tabView.removeTab(styleData.index)
                        }
                    }
                }
            }
    }
}
