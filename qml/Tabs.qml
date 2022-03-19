import QtQuick 2.6
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.2

TabView {
    id: tabView


    property Item activeTabItem
    property Component item_component
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
        tabView.addTab("", comp);
        tabView.currentIndex = tabView.count - 1;
        var tab = tabView.getTab(tabView.currentIndex)
        var title = tab.item.title ? tab.item.title : "Shell " + tabView.count
        tab.item.titleChanged.connect(_updateTabTitle.bind(tab.item))
        tab.title = title

        fixupVisibility()
    }

    style: TabViewStyle {
            id: main_style
            property color frameColor: "#999"
            property color fillColor: "#eee"
            property int plate_width:0
            property int sum_width:0
            property int overl: 0
            tabsMovable: true
            tabOverlap: overl
            frame: Rectangle {
                color: "#eee"
                border.color: frameColor
            }
            tab: Rectangle {
                id:tabplate
                color: styleData.selected ? fillColor : frameColor
                implicitWidth: Math.max(text.width + 24, 80)
                implicitHeight: 20
                Component.onCompleted: {
                    if (styleData.totalWidth === 0 ){
                        main_style.sum_width = tabplate.width;
                        main_style.plate_width = styleData.totalWidth;}
                    else {
                        var delta = styleData.totalWidth - main_style.plate_width;
                        main_style.sum_width = main_style.sum_width + delta;
                        main_style.plate_width = styleData.totalWidth;
                    }
                }
                onWidthChanged: {
                    if (styleData.totalWidth === 80 ){
                        main_style.sum_width = tabplate.width;}

                }
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
                            {
                                tabView.removeTab(styleData.index);
                                main_style.sum_width = main_style.sum_width - (styleData.totalWidth - main_style.plate_width);
                                main_style.plate_width = main_style.plate_width - (styleData.totalWidth - main_style.plate_width);
                            }
                            else{
                                window.close();
                            }
                        }
                    }
                }
            }
            tabBar: BarTab{
                property var backColor: "gray"
            }

    }
}
