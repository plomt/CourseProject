import QtQuick 2.0

Rectangle{
    color: backColor

               Rectangle{
                   id: newTab
                   implicitHeight: 19
                   implicitWidth: 50
                   color: parent.color
                   anchors.bottom:parent.bottom
                   x: main_style.sum_width
                   Rectangle{
                       id:but
                       implicitHeight: parent.height
                       implicitWidth: parent.width / 2 - 2
                       anchors.right:parent.BottomLeft
                       color:parent.color
                       Image {
                           id: add
                           anchors.centerIn: parent
                           source: "./plus.png"
                           width: parent.width
                           height: parent.height
                       }
                       MouseArea {
                           anchors.fill: parent
                           hoverEnabled: true
                           onClicked: {
                               var delta = main_style.sum_width - main_style.plate_width;
                               if (dropdown.state === "dropDown")
                                   dropdown.state = "";
                               else if (window.width - newTab.x - params.width - 14 > delta)
                                        {
                                            tabView.createTab(item_component);
                                            seanceModel.update("1")
                                        }
                           }
                           onEntered: {
                               parent.color = "#2b2625"
                           }
                           onExited: {
                               parent.color = "gray"
                           }
                       }
                   }
                   Rectangle{
                       id: params
                       implicitHeight: parent.height
                       implicitWidth: parent.width / 2 - 2
                       anchors.left:but.right
                       color:parent.color
                       Image {
                           id: more
                           anchors.centerIn: parent
                           source: "./triangle.png"
                           width: parent.width - 10
                           height: parent.height - 10
                       }
                       Shtorka{
                           id: dropdown
                           anchors.top:parent.bottom
                       }
                       MouseArea {
                           anchors.fill: parent
                           hoverEnabled: true
                           onClicked: {
                               dropdown.state = dropdown.state==="dropDown"?"":"dropDown"
                           }
                           onEntered: {
                               parent.color = "#2b2625"
                           }
                           onExited: {
                               parent.color = backColor
                           }
                       }
                   }
                   Connections{
                        target: tabCreator
                        function onAddTab() {
                            var delta = main_style.sum_width - main_style.plate_width;
                                  if (window.width - newTab.x - params.width - 14 > delta)
                                  {
                                    tabView.createTab(item_component);
                                    seanceModel.update("1")
                                  }
                        }
                   }
          }
}
