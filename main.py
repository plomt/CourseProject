import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtQuick import QQuickPaintedItem, QQuickItem

from textRender import MyTerm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qmlRegisterType(MyTerm, 'Terminal', 1, 0, 'MyTerm')
    engine = QQmlApplicationEngine('./qml/base.qml')
    sys.exit(app.exec_())
