import QtQuick 2.6
import QtQuick.Window 2.2
import QtQuick.Controls 2.4

ApplicationWindow {
    id: window
    width: 640
    height: 480
    title: "Terminal"
    visible: true
    minimumWidth: 320
    minimumHeight: 240
    color: "#000000"

    property int fontSize: 14*pixelRatio
    property real pixelRatio: 1.0
    property int buttonWidthSmall: 60*pixelRatio
    property int buttonWidthLarge: 180*pixelRatio
    property int buttonWidthHalf: 90*pixelRatio

    property int buttonHeightSmall: 48*pixelRatio
    property int buttonHeightLarge: 68*pixelRatio

    property int headerHeight: 20*pixelRatio

    property int radiusSmall: 5*pixelRatio
    property int radiusMedium: 10*pixelRatio
    property int radiusLarge: 15*pixelRatio

    property int paddingSmall: 5*pixelRatio
    property int paddingMedium: 10*pixelRatio

    property int fontSizeSmall: 14*pixelRatio
    property int fontSizeLarge: 24*pixelRatio


}
