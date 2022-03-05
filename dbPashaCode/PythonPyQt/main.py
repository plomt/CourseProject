import os
import sys

from peewee import *

from utils import (
    Configuration,
    manipulation_database
)
from model import *

CUR_PATH = os.getcwd()
if sys.platform == 'win32':
    os.environ['CONFIG_PATH'] = CUR_PATH + r"\settings\settings.yml"

    conf = Configuration()
    SCHEMA_SCRIPTS = CUR_PATH + conf["PATHS"]["SCHEMA_PATH_WIN32"]
    TABLE_SCRIPTS = CUR_PATH + conf["PATHS"]["TABLE_PATH_WIN32"]
else:
    os.environ['CONFIG_PATH'] = CUR_PATH + "/settings/settings.yml"

    conf = Configuration()
    SCHEMA_SCRIPTS = CUR_PATH + conf["PATHS"]["SCHEMA_PATH_LINUX"]
    TABLE_SCRIPTS = CUR_PATH + conf["PATHS"]["TABLE_PATH_LINUX"]


# os.system(r"python -m pwiz -e postgresql -u postgres -s project_pyqt -P 0000 postgres > C:\Users\pavel\PycharmProjects\PythonPyQt\model.py")

# def main():
#     for script in [SCHEMA_SCRIPTS + "\create_schema.sql", TABLE_SCRIPTS + "\create_tables.sql"]:
#         manipulation_database(script)
#
# main()
