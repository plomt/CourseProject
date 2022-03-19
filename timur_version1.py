from re import S
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import getpass
import socket
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRect, Qt, pyqtSignal, QRegExp
import subprocess
import traceback

from dbPashaCode.PythonPyQt.model import *
from dbPashaCode.PythonPyQt.utils import *

from datetime import datetime

# lineBarColor = QColor(53, 53, 53)


class PlainTextEdit(QPlainTextEdit):
    commandSignal = pyqtSignal(str)
    commandZPressed = pyqtSignal(str)

    def __init__(self, parent=None, movable=False):
        super().__init__(parent)

        self.name = "[" + str(getpass.getuser()) + "@" + str(socket.gethostname()) + "]" + "  ~" + str(
            os.getcwd()) + " >$ "
        self.appendPlainText(self.name)
        self.movable = movable
        self.parent = parent
        self.commands = []  # This is a list to track what commands the user has used so we could display them when
        # up arrow key is pressed
        self.tracker = 0
        self.setStyleSheet("QPlainTextEdit{background-color: #212121; color: white; padding: 8;}")
        self.font = QFont()
        self.font.setFamily("Iosevka")
        self.font.setPointSize(12)
        self.text = None
        self.setFont(self.font)
        self.document_file = self.document()
        self.previousCommandLength = 0
        self.document_file.setDocumentMargin(-1)

        

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        if self.movable is True:
            self.parent.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.movable is True:
            self.parent.mouseMoveEvent(event)

    def textUnderCursor(self):
        textCursor = self.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)

        return textCursor.selectedText()

    def keyPressEvent(self, e):
        cursor = self.textCursor()

        if self.parent:

            if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_A:
                return

            if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Z:
                self.commandZPressed.emit("True")
                return

            if e.key() == 16777220:  # This is the ENTER key
                text = self.textCursor().block().text()

                if text == self.name + text.replace(self.name, "") and text.replace(self.name, "") != "":  # This is to prevent adding in commands that were not meant to be added in
                    self.commands.append(text.replace(self.name, ""))
                self.commandSignal.emit(text)
                self.appendPlainText(self.name)

                return

            if e.key() == Qt.Key_Up:
                try:
                    if self.tracker != 0:
                        cursor.select(QTextCursor.BlockUnderCursor)
                        cursor.removeSelectedText()
                        self.appendPlainText(self.name)

                    self.insertPlainText(self.commands[self.tracker])
                    self.tracker += 1

                except IndexError:
                    self.tracker = 0

                return

            if e.key() == Qt.Key_Down:
                try:
                    cursor.select(QTextCursor.BlockUnderCursor)
                    cursor.removeSelectedText()
                    self.appendPlainText(self.name)

                    self.insertPlainText(self.commands[self.tracker])
                    self.tracker -= 1

                except IndexError:
                    self.tracker = 0

            if e.key() == 16777219:
                if cursor.positionInBlock() <= len(self.name):
                    return

                else:
                    cursor.deleteChar()

            super().keyPressEvent(e)

        e.accept()


class Color_LineEdit(QLineEdit):
    commandEnterPressed = pyqtSignal(str)
    def __init__(self, parent=None, movable=False):
        super().__init__(parent)
        self.setPlaceholderText("Enter color. Example: black, cyan")

    def keyPressEvent(self, e):
        # cursor = self.textCursor()

        if e.key() == 16777220:  # This is the ENTER key
            self.commandEnterPressed.emit("True")

            return
        super().keyPressEvent(e)

    

        
class Terminal(QWidget):
    errorSignal = pyqtSignal(str)
    outputSignal = pyqtSignal(str)

    def __init__(self, movable=False):
        super().__init__()
        # self.setWindowFlags(
        #     Qt.Widget |
        #     Qt.WindowCloseButtonHint |
        #     Qt.WindowStaysOnTopHint |
        #     Qt.FramelessWindowHint
        # )
        # self.toolbar = self.addToolBar('Toolbar')
       

        self.id_seance = 'DEFAULT'
        self.id_login = 'DEFAULT'

    
        self.movable = movable
        self.process = QProcess(self)
        self.editor = PlainTextEdit(self, self.movable)
        # self.layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.name = None
        self.highlighter = name_highlighter(self.editor.document(), str(getpass.getuser()), str(socket.gethostname()), str(os.getcwd()))
        self.layout.addWidget(self.editor, 0)

        self.saltLine = Color_LineEdit()
        # self.saltLine.setPlaceholderText("Enter user name")
        # self.saltLine.keyPressEvent()
        self.saltLine.commandEnterPressed.connect(self.push_color_change_scene)
        self.layout.addWidget(self.saltLine, 0.5)


        self.editor.commandSignal.connect(self.handle)
        self.editor.commandZPressed.connect(self.handle)
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)

        # self.push_change.clicked.connect(self.push_change_scene)

        # self.toolBar = QToolBar()
        # self.layout.addWidget(self.toolBar)

        self.setLayout(self.layout)
        self.window_width, self.window_height = 1000, 600
        self.setMinimumSize(self.window_width, self.window_height)


    def push_color_change_scene(self):
        str_colors = self.saltLine.text().split(', ')
        back_color = str_colors[0]
        color_of_text = str_colors[1]
        str_text = "QPlainTextEdit {background-color: " + back_color + "; color: " + color_of_text + ";}"
        self.editor.setStyleSheet(str_text)
        pass

    def get_id_login(self):
        self.editor.appendPlainText(str(self.id_login))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)

        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def onReadyReadStandardError(self):
        self.error = self.process.readAllStandardError().data().decode()
        self.editor.appendPlainText(self.error.strip('\n'))
        self.errorSignal.emit(self.error)
        print("errr")


    def onReadyReadStandardOutput(self):
        self.result = self.process.readAllStandardOutput().data().decode()
        self.editor.appendPlainText(self.result.strip('\n'))
        self.state = self.process.state()
        self.outputSignal.emit(self.result)

    def run(self, command):
        """Executes a system command."""
        self.process.start(command)

    def handle(self, command):
        
        """Split a command into list so command echo hi would appear as ['echo', 'hi']"""
        real_command = command.replace(self.editor.name, "")

        if command == "True":
            if self.process.state() == 2:
                self.process.kill()

        if real_command != "":
            command_list = real_command.split()
        else:
            command_list = None
        """Now we start implementing some commands"""
        if real_command == "clear":
            self.editor.clear()
        elif "&&" in command_list:
            pass
            # print(command_list)
            # print(command_list.index("&&"))
            #print(command_list[command_list.index("&&")+1:])
        elif command_list is not None and command_list[0] == "echo":
            self.editor.appendPlainText(" ".join(command_list[1:]))
        elif real_command == "exit":
            self.close()
            # qApp.exit()

        elif command_list is not None and command_list[0] == "cd" and len(command_list) > 1:
            try:
                os.chdir(" ".join(command_list[1:]))
                self.editor.name = "[" + str(getpass.getuser()) + "@" + str( socket.gethostname()) + "]" + "  ~" + str(os.getcwd()) + " >$ "
                if self.highlighter:
                    del self.highlighter
                self.highlighter = name_highlighter(self.editor.document(), str(getpass.getuser()), str(socket.gethostname()), str(os.getcwd()))

            except FileNotFoundError as E:
                self.editor.appendPlainText(str(E))

        elif len(command_list) == 1 and command_list[0] == "cd":

            os.chdir(str(Path.home()))
            self.editor.name = "[" + str(getpass.getuser()) + "@" + str( socket.gethostname()) + "]" + "  ~" + str(os.getcwd()) + " >$ "

        elif self.process.state() == 2:
            self.process.write(real_command.encode())
            print("wrote") 
            self.process.closeWriteChannel()
            

        elif command == self.editor.name + real_command:

            if real_command[:21] == 'change_color_terminal':
                # otherFormat = QTextCharFormat()
                # otherFormat.setForeground(QColor(command_list[1]))
                str_text = "QPlainTextEdit {background-color: " + command_list[1] + "; color: " + command_list[2] + ";}"
                self.editor.setStyleSheet(str_text)
                # self.editor.setStyleSheet("QPlainTextEdit {background-color: black; color: red;}")
                # print('ahahah')
                # print(command_list)
                

            else:#команда
                sp = subprocess.Popen(real_command, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
                out, err = sp.communicate()

                command = real_command
                date_time = str(datetime.today())
                name_user = self.id_login
                session_id = str(self.id_seance)
                # print(name_user, session_id)
                # print('тип ', type(name_user), type(session_id))

                if out:
                    #---------------------------------------------------------------------------------------------------------------
                    
                    answer_to_command = str(out.decode('cp866'))
                    flag = True
                    table_message = Message(command=command, answer_to_command=answer_to_command, flag=flag, date_time=date_time, id_seance=session_id)
                    table_message.save()
                    # self.session_id = "id:" + str(session_id) + ";user:" + name_user #ID
                    # ---------------------------------------------------------------------------------------------------------------

                    # self.get_id_login()
                    self.editor.appendPlainText(str(out.decode('cp866')))
                if err:
                    #---------------------------------------------------------------------------------------------------------------
                    
                    answer_to_command = str(err.decode('cp866'))
                    flag = False
                    table_message = Message(command=command, answer_to_command=answer_to_command, flag=flag, date_time=date_time, id_seance=session_id)
                    table_message.save()
                    # self.session_id = "id:" + str(session_id) + ";user:" + name_user #ID
                    # ---------------------------------------------------------------------------------------------------------------

                    self.editor.appendPlainText(str(err.decode('cp866')))

        
        

        else:
            pass # When the user does a command like ls and then presses enter then it wont read the line where the cursor is on as a command

    def change_user(self):
        self.setWindowTitle(f"{self.id_seance}_{self.id_login}")


class name_highlighter(QSyntaxHighlighter):
    

    def __init__(self, parent=None, user_name=None, host_name=None, cwd=None):
        super().__init__(parent)
        self.highlightingRules = []
        self.name = user_name
        self.name2 = host_name
        self.cwd = cwd
        #print(self.cwd)
        first_list = []
        most_used = ["cd", "clear", "history", "ls", "man", "pwd", "what", "type",
        "strace", "ltrace", "gdb", "cat", "chmod", "cp", "chown", "find", "grep", "locate", "mkdir", "rmdir", "rm", "mv", "vim", "nano", "rename",
        "touch", "wget", "zip", "tar", "gzip", "apt", "bg", "fg", "df", "free", "ip", "jobs", "kill", "killall", "mount", "umount", "ps", "sudo", "echo",
        "top", "uname", "whereis", "uptime", "whereis", "whoami", "exit"
        ]

        self.regex = {
            "class": "\\bclass\\b",
            "function": "[A-Za-z0-9_]+(?=\\()",
            "magic": "\\__[^']*\\__",
            "decorator": "@[^\n]*",
            "singleLineComment": "#[^\n]*",
            "quotation": "\"[^\"]*\"",
            "quotation2": "'[^\']*\'",
            "multiLineComment": "[-+]?[0-9]+",
            "int": "[-+]?[0-9]+",
        }
        """compgen -c returns all commands that you can run"""

        for f in most_used:
            nameFormat = QTextCharFormat()
            nameFormat.setForeground(QColor("#00ff00"))
            nameFormat.setFontItalic(True)
            self.highlightingRules.append((QRegExp("\\b" + f + "\\b"), nameFormat))

        otherFormat = QTextCharFormat()
        otherFormat.setForeground(QColor("#f7797d"))
        self.highlightingRules.append((QRegExp("~\/[^\s]*"), otherFormat))


        hostnameFormat = QTextCharFormat()
        hostnameFormat.setForeground(QColor("#f7797d"))

        self.highlightingRules.append((QRegExp(self.name), hostnameFormat))
        self.highlightingRules.append((QRegExp(self.name2), hostnameFormat))
        quotation1Format = QTextCharFormat()

        quotation1Format.setForeground(QColor("#96c93d"))
        self.highlightingRules.append((QRegExp("\"[^\"]*\""), quotation1Format))

        quotation2Format = QTextCharFormat()
        quotation2Format.setForeground(QColor("#96c93d"))
        self.highlightingRules.append((QRegExp("'[^\']*\'"), quotation2Format))

        integerFormat = QTextCharFormat()
        integerFormat.setForeground(QColor("#cc5333"))
        integerFormat.setFontItalic(True)
        self.highlightingRules.append((QRegExp("\\b[-+]?[0-9]+\\b"), integerFormat))

    def highlightBlock(self, text):
        

        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class seance_window(QWidget):
    def __init__(self):
        super().__init__()
        # self.id_deance
        self.id_seance = '-1'
        self.login = 'DEFAULT'

        self.text = QTextBrowser()

        # arr = ["echo 'alalal' ", "dir", "path"]
        # set_text()
        str_text = "QTextBrowser {background-color: " + 'black' + "; color: " + 'cyan' + ";}"
        self.setStyleSheet(str_text)
         
        str_text = "QWidget { background-color: black; color: cyan; }"
        self.setStyleSheet(str_text)


        grid = QVBoxLayout()
        self.setLayout(grid)
        grid.addWidget(self.text, 0)

        self.push_b = QPushButton("&delete", self)
        grid.addWidget(self.push_b, 0)

        self.push_b.clicked.connect(self.push_delete)


        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Simple menu')

    def push_delete(self):
        # удаляем данные из базы
        pass
        

    def set_id_and_login(self, id, login):
        self.id_seance = id
        self.login = login

    def set_text(self):
        # arr = [self.id_seance, self.login]
        # str_arr = '\n'.join(arr)

        query = Message.select().where(Message.id_seance == int(self.id_seance))
        print(query)
        arr = [message.command + ' - ' + message.answer_to_command for message in query]
        print(arr)

        str_arr = '\n'.join(arr)
        print(str_arr)

        self.text.setText(str_arr)



class Login_LineEdit(QLineEdit):
    commandEnterPressed = pyqtSignal(str)
    def __init__(self, parent=None, movable=False):
        super().__init__(parent)
        self.setPlaceholderText("Enter the user name")

    def keyPressEvent(self, e):
        # cursor = self.textCursor()

        if e.key() == 16777220:  # This is the ENTER key
            self.commandEnterPressed.emit("True")

            return
        super().keyPressEvent(e)





class Example(QMainWindow):
    # widget = Terminal(True)
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")

        str_text = "QWidget { background-color: black; color: cyan; }"
        self.setStyleSheet(str_text)
        
        self.Login = 'DEFAULT'
        self.seance = '-1'

        self.saltLine = Login_LineEdit()
        self.saltLine.setPlaceholderText("Enter user name")
        self.saltLine.commandEnterPressed.connect(self.push_login_scene)



        grid = QVBoxLayout()#QGridLayout()
        widget = QWidget()
        widget.setLayout(grid)


        self.listWidget = QListWidget(self)

        #ПАША ДАЙ МНЕ СПИСОК СЕАНСОВ ИЗ БД

        query = Seance.select()
        print([(seance.id_seance, seance.name_user) for seance in query])

        arr = [str(seance.id_seance) + '_' + seance.name_user for seance in query]

        for i in arr:
            self.listWidget.addItem(i) 

        #add your widgets
        self.setCentralWidget(widget)
        grid.addWidget(self.listWidget, 0)
        grid.addWidget(self.saltLine, 1)
        self.listWidget.itemClicked.connect(self.item_clicked)
        
        

        self.toolbar = self.addToolBar('Toolbar')
        
        about_us_Action = QAction('About Us', self)
        about_us_Action.triggered.connect(self.about_us)
        
        self.toolbar.addAction(about_us_Action)

        refresh = QAction('Refresh', self)
        refresh.triggered.connect(self.refresh)
        
        self.toolbar.addAction(refresh)
        


        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Simple menu')
        self.show()

    def about_us(self):
        print('Делали: Верендеев Илья, Кондаков Александр, Ломтев Павел, Тухватуллин Тимур')
        self.listWidget.clear()
        self.listWidget.addItem('Делали: \nВерендеев Илья, \nКондаков Александр, \nЛомтев Павел, \nТухватуллин Тимур \nНажмите REFRESH для обновления')

    def refresh(self):
        query = Seance.select()
        print([(seance.id_seance, seance.name_user) for seance in query])

        arr = [str(seance.id_seance) + '_' + seance.name_user for seance in query]
        self.listWidget.clear()

        for i in arr:
            self.listWidget.addItem(i) 

    def item_clicked(self, item):
        self.dialog_seance = seance_window()
        id, user = item.text().split('_')
        self.dialog_seance.set_id_and_login(id, user)
        self.dialog_seance.show()
        self.dialog_seance.set_text()

    
    @pyqtSlot()
    def push_login_scene(self):
        # self.saltLine.setPlaceholderText("e.g. ahahahah")
        print('PyQt5 button click')
        print(self.saltLine.text())
        
        self.Login = self.saltLine.text()
        
        #---------------------------------------------------------------------------------------------------------------
        name_user = self.Login

        table_seance = Seance(name_user=name_user)
        table_seance.save()

        # ---------------------------------------------------------------------------------------------------------------
        self.seance = Seance.select(fn.MAX(Seance.id_seance)).scalar()
        if self.seance is None:
            self.seance = '1'

        self.dialog = Terminal()
        self.dialog.id_login = self.Login
        self.dialog.id_seance = self.seance
        self.dialog.change_user()
        self.dialog.show()





    # def onAction1(self):
    #     self.close()




def main():
    app = QApplication(sys.argv)
    ex = Example()
    # ex = seance_window()
    # ex.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
    
