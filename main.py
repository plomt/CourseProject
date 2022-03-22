import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtQuick import QQuickPaintedItem, QQuickItem

from textRender import MyTerm

from Seances import seanceListModel, seanceTable, tabCreator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qmlRegisterType(MyTerm, 'Terminal', 1, 0, 'MyTerm')

    engine = QQmlApplicationEngine()
    seanceModel = seanceListModel()
    commandTable = seanceTable()
    tabs = tabCreator()

    context = engine.rootContext()
    context.setContextProperty("seanceModel", seanceModel)
    context.setContextProperty("seanceTable", commandTable)
    context.setContextProperty("tabCreator", tabs)
    engine.load('./qml/base.qml')
    seanceModel.update("complete")
    sys.exit(app.exec_())
