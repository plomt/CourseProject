from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtQuick import QQuickPaintedItem, QQuickItem

from Terminal import Terminal


class MyTerm(QQuickPaintedItem):

    titleChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.terminal = Terminal(True)
        self.editor = self.terminal.editor

        self.setFlag(QQuickItem.ItemHasContents, True)
        self.setFlag(QQuickItem.ItemAcceptsInputMethod, True)
        self.setFlag(QQuickItem.ItemIsFocusScope, True)

        self.setAcceptedMouseButtons(Qt.AllButtons)
        self.editor.installEventFilter(self)
        self.widthChanged.connect(self.updateWidgetSize)
        self.heightChanged.connect(self.updateWidgetSize)
        self.fillColorChanged.connect(self.changeColor)

        self._title = self.terminal.session_id
        self.titleChanged.emit()

    @pyqtProperty(QColor)
    def color(self):
        return self.fillColor()

    @color.setter
    def color(self, color):
        self.setFillColor(color)

    @pyqtProperty(str, notify=titleChanged)
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        self.titleChanged.emit()

    def event(self, event):
        if event.type() == QEvent.FocusIn:
            self.forceActiveFocus()
            return QQuickPaintedItem.event(self, event)
        elif event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseMove:
            self.processMouseEvent(event)
            return True
        elif event.type() == QEvent.KeyPress:
            self.processKeyEvent(event)
            return True
        elif event.type() == QEvent.Wheel:
            self.editor.wheelEvent(event)
            return True
        return QApplication.sendEvent(self.terminal, event)

    def paint(self, painter):
        if painter is not None:
            self.terminal.render(painter)

    def eventFilter(self, a0, event) -> bool:
        if a0 == self.editor or a0 is self.editor:
            if event.type() == QEvent.Paint or event.type() == QEvent.UpdateRequest:
                self.update()
        return QQuickPaintedItem.eventFilter(self, a0, event)

    def updateWidgetSize(self):
        self.terminal.setFixedSize(self.width().__int__(), self.height().__int__())
        self.update()

    def changeColor(self):
        p = self.editor.palette()
        new_col = self.fillColor()
        # new_col = self._color
        p.setColor(QPalette.Active, QPalette.Base, new_col)
        self.editor.setPalette(p)
        self.update()

    def processMouseEvent(self, event):
        if event.type() == QEvent.MouseButtonPress:
            self.editor.mousePressEvent(event)
        elif event.type() == QEvent.MouseMove:
            self.editor.mouseMoveEvent(event)

    def processKeyEvent(self, event):
        self.editor.keyPressEvent(event)
