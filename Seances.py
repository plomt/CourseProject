from PyQt5 import QtCore, QtGui, QtQuick
from PyQt5.QtCore import QAbstractListModel,Qt, QModelIndex, QVariant, QAbstractTableModel,pyqtSlot


from dbPashaCode.PythonPyQt.model import *
from dbPashaCode.PythonPyQt.utils import *

class Model(QAbstractListModel):
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.seances = []
        self.schema = [
            b"pyLabel"
        ]

    @pyqtSlot(str)
    def update(self, string):
        if string == "complete":
            query = Seance.select().dicts()
            self.beginResetModel()
            for row in query:
                self.seances.append(str(row['id_seance']) + " " + str(row['name_user']))
            self.endResetModel()
        else:
            query = Seance.select(fn.MAX(Seance.id_seance)).scalar()
            query = Seance.select().where(Seance.id_seance == query)
            self.beginResetModel()
            msg = [[message.id_seance, message.name_user] for message in query]
            self.seances.append(str(msg[0][0]) +" "+ str(msg[0][1]))
            self.endResetModel()


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

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            return f"Test {section}"

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


#query = Message.select().where(Message.id_seance == 72)
#print([(message.command, message.answer_to_command, message.date_time) for message in query])
#query = Seance.select(fn.MAX(Seance.id_seance)).scalar()
#query = Seance.select().where(Seance.id_seance == query)
#print([[message.id_seance, message.name_user] for message in query])