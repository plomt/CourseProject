import subprocess
import shlex
import sys, platform
from PyQt5.QtCore import pyqtSignal, QObject
from signal import signal, SIGINT

def is_cmd(name):
    """Check whether `name` is on PATH."""
    from distutils.spawn import find_executable
    return find_executable(name) is not None


class Terminal(QObject):

    out = pyqtSignal(str)
    proc_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.proc = None

    def process_cmd(self, cmdline):
        if platform.system() == 'Windows':
            cmd = cmdline
            code_page = "866"
        else:
            cmd = shlex.split(cmdline)
            code_page = "utf-8"
        self.proc = subprocess.Popen(cmd, shell=True, encoding=code_page, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, errors='replace')
        while True:
            realtime_output = self.proc.stdout.readline()
            if realtime_output == '' and self.proc.poll() is not None:
                break
            if realtime_output:
                print(realtime_output.strip(), flush=False)
                sys.stdout.flush()

    def send_signal(self, sig):
        if self.proc is not None:
            self.proc.send_signal(sig)


