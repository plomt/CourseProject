from PyQt5 import QtCore, QtGui, QtQuick
from PyQt5.QtCore import QAbstractListModel,Qt, QModelIndex, QVariant, QAbstractTableModel,pyqtSlot,pyqtSignal, QObject


from dbPashaCode.PythonPyQt.model import *
from dbPashaCode.PythonPyQt.utils import *

class seanceListModel(QAbstractListModel):

    seanceDeleted = pyqtSignal(str)

    def __init__(self, parent=None):
        super(seanceListModel, self).__init__(parent)
        self.seances = []
        self.schema = [
            b"pyLabel"
        ]

    @pyqtSlot(str)
    def update(self, string):
        if string == "complete":
            query = Seance.select().dicts()
            self.beginResetModel()
            self.seances = []
            for row in query:
                self.seances.append(str(row['id_seance']) + " " + str(row['name_user']))
            self.seances.sort()
            self.endResetModel()
        elif string == "1":
            query = Seance.select(fn.MAX(Seance.id_seance)).scalar()
            query = Seance.select().where(Seance.id_seance == query)
            self.beginResetModel()
            msg = [[message.id_seance, message.name_user] for message in query]
            self.seances.append(str(msg[0][0]) +" "+ str(msg[0][1]))
            self.seances.sort()
            self.endResetModel()

    @pyqtSlot(str)
    def delete(self, string):
        self.beginResetModel()
        id_seance = int(string.split(' ')[0])
        query = Seance.delete().where(Seance.id_seance == id_seance)
        query.execute()
        query = Message.delete().where(Message.id_seance == id_seance)
        query.execute()
        self.seances.remove(string)
        self.endResetModel()
        self.seanceDeleted.emit(str(id_seance))

    def data(self, index, role):
            return self.seances[index.row()]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.seances)

    def roleNames(self):
        """Role names are used by QML to map key to role"""
        return dict(enumerate(self.schema))


class seanceTable(QAbstractTableModel):


    _data = []
    def __init__(self, parent=None):
        super(seanceTable, self).__init__(parent)


    @pyqtSlot(str)
    def update(self, id_seance):
        self.beginResetModel()
        id_seance = int(id_seance)
        query = Message.select().where(Message.id_seance == id_seance)
        self._data = [[message.command, message.answer_to_command, message.date_time] for message in query]
        self.endResetModel()

    @pyqtSlot()
    def clearTable(self):
        self.beginResetModel()
        self._data = []
        self.endResetModel()

    @pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return f"Коман\nда"
                if section == 1:
                    return f"Ответ"
                if section == 2:
                    return f"Время"
        return QVariant()

    def data(self, index, role):
        if not self._data:
            return QVariant()
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return QVariant()

    def rowCount(self, index):
        if not self._data:
            return 0
        else:
            return len(self._data)

    def columnCount(self, index):
        if not self._data:
            return 0
        else:
            return len(self._data[0])

    def roleNames(self):
        roles = {
            Qt.DisplayRole: b'display'
        }
        return roles


class tabCreator(QObject):

    addTab = pyqtSignal()
    newWin = pyqtSignal()
    changeTab = pyqtSignal(str)

    cur_id = ""
    def __init__(self, parent=None):
        super(tabCreator, self).__init__(parent)
        self.new_tab = True

    @pyqtSlot()
    def newSeance(self):
        if self.new_tab is True:
            self.addTab.emit()
        else:
            self.newWin.emit()

    @pyqtSlot(str)
    def changeState(self, state):
        if state == "True":
            self.new_tab = True
        else:
            self.new_tab = False

    @pyqtSlot(str)
    def switchTab(self, id):
        self.changeTab.emit(id)