import sys
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, QVariant,pyqtProperty
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from Exec import Terminal


if __name__ == '__main__':

    #app = QApplication(sys.argv)
    #engine = QQmlApplicationEngine('./qml/base.qml')

    ter = Terminal()
    ter.process_cmd("ping www.yahoo.com")
    #sys.exit(app.exec_())


