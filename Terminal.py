import sys
import os
import getpass
import socket
from pathlib import Path
import subprocess

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from datetime import datetime

from dbPashaCode.PythonPyQt.model import *
from dbPashaCode.PythonPyQt.utils import *


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
        self.setStyleSheet("QPlainTextEdit{color: white; }")
        self.font = QFont()
        self.font.setFamily("Iosevka")
        self.font.setPointSize(12)
        self.text = None
        self.setFont(self.font)
        self.document_file = self.document()
        self.previousCommandLength = 0
        self.document_file.setDocumentMargin(-1)

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

                if text == self.name + text.replace(self.name, "") and text.replace(self.name,
                                                                                    "") != "":  # This is to prevent adding in commands that were not meant to be added in
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


class Terminal(QWidget):
    errorSignal = pyqtSignal(str)
    outputSignal = pyqtSignal(str)

    def __init__(self, movable=False):
        super().__init__()
        self.movable = movable
        self.process = QProcess(self)
        self.editor = PlainTextEdit(self, self.movable)
        # self.layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.name = None
        self.highlighter = name_highlighter(self.editor.document(), str(getpass.getuser()), str(socket.gethostname()),
                                            str(os.getcwd()))
        self.layout.addWidget(self.editor)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.editor.commandSignal.connect(self.handle)
        self.editor.commandZPressed.connect(self.handle)
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
        self.setLayout(self.layout)
        self.window_width, self.window_height = 640, 480
        self.setMinimumSize(self.window_width, self.window_height)


        #---------------------------------------------------------------------------------------------------------------
        name_user = os.getlogin()

        table_seance = Seance(name_user=name_user)
        table_seance.save()

        session_id = Seance.select(fn.MAX(Seance.id_seance)).scalar()
        self.id_seance = session_id
        # ---------------------------------------------------------------------------------------------------------------

        self.session_id = "Seance " + str(session_id) + " " + str(datetime.now().strftime("%H:%M")) + " "


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

        real_command = command.replace(self.editor.name, "")

        if command == "True":
            if self.process.state() == 2:
                self.process.kill()

        if real_command != "":
            command_list = real_command.split()
        else:
            command_list = None
        if real_command == "clear":
            self.editor.clear()
        elif command_list is not None and "&&" in command_list:
            pass
            # print(command_list)
            # print(command_list.index("&&"))
            # print(command_list[command_list.index("&&")+1:])
        elif command_list is not None and command_list[0] == "echo":
            self.editor.appendPlainText(" ".join(command_list[1:]))
        elif real_command == "exit":
            self.close()


        elif command_list is not None and command_list[0] == "cd" and len(command_list) > 1:
            try:
                os.chdir(" ".join(command_list[1:]))
                self.editor.name = "[" + str(getpass.getuser()) + "@" + str(socket.gethostname()) + "]" + "  ~" + str(
                    os.getcwd()) + " >$ "
                if self.highlighter:
                    del self.highlighter
                self.highlighter = name_highlighter(self.editor.document(), str(getpass.getuser()),
                                                    str(socket.gethostname()), str(os.getcwd()))

            except FileNotFoundError as E:
                self.editor.appendPlainText(str(E))

        elif command_list is not None and len(command_list) == 1 and command_list[0] == "cd":

            os.chdir(str(Path.home()))
            self.editor.name = "[" + str(getpass.getuser()) + "@" + str(socket.gethostname()) + "]" + "  ~" + str(
                os.getcwd()) + " >$ "

        elif self.process.state() == 2:
            self.process.write(real_command.encode())
            print("wrote")
            self.process.closeWriteChannel()
        elif command == self.editor.name + real_command:

            if real_command[:21] == 'change_color_terminal':
                str_text = "QPlainTextEdit {background-color: " + command_list[1] + "; color: " + command_list[2] + ";}"
                self.editor.setStyleSheet(str_text)
                print(command_list)

            else:  # ??????????????
                sp = subprocess.Popen(real_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = sp.communicate()

                command = real_command
                date_time = str(datetime.today())
                #name_user = self.id_login
                session_id = str(self.id_seance)
                # print(name_user, session_id)
                # print('?????? ', type(name_user), type(session_id))

                if out:
                    # ---------------------------------------------------------------------------------------------------------------

                    answer_to_command = str(out.decode('cp866'))
                    flag = True
                    table_message = Message(command=command, answer_to_command=answer_to_command, flag=flag,
                                            date_time=date_time, id_seance=session_id)
                    table_message.save()
                    # self.session_id = "id:" + str(session_id) + ";user:" + name_user #ID
                    # ---------------------------------------------------------------------------------------------------------------

                    # self.get_id_login()
                    self.editor.appendPlainText(str(out.decode('cp866')))
                if err:
                    # ---------------------------------------------------------------------------------------------------------------

                    answer_to_command = str(err.decode('cp866'))
                    flag = False
                    table_message = Message(command=command, answer_to_command=answer_to_command, flag=flag,
                                            date_time=date_time, id_seance=session_id)
                    table_message.save()
                    self.editor.appendPlainText(str(err.decode('cp866')))
        else:
            pass

        self.editor.ensureCursorVisible()

class name_highlighter(QSyntaxHighlighter):

    def __init__(self, parent=None, user_name=None, host_name=None, cwd=None):
        super().__init__(parent)
        self.highlightingRules = []
        self.name = user_name
        self.name2 = host_name
        self.cwd = cwd
        first_list = []
        most_used = ["cd", "clear", "history", "ls", "man", "pwd", "what", "type",
                     "strace", "ltrace", "gdb", "cat", "chmod", "cp", "chown", "find", "grep", "locate", "mkdir",
                     "rmdir", "rm", "mv", "vim", "nano", "rename",
                     "touch", "wget", "zip", "tar", "gzip", "apt", "bg", "fg", "df", "free", "ip", "jobs", "kill",
                     "killall", "mount", "umount", "ps", "sudo", "echo",
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