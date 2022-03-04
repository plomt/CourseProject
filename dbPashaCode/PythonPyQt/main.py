import os
from utils import (
    Configuration,
    manipulation_database
)

CUR_PATH = r"C:\Users\pavel\PycharmProjects\PythonPyQt"
os.environ['CONFIG_PATH'] = CUR_PATH + r"\settings\settings.yml"

conf = Configuration()
SCHEMA_SCRIPTS = CUR_PATH + conf["PATHS"]["SCHEMA_PATH"]
TABLE_SCIPTS = CUR_PATH + conf["PATHS"]["TABLE_PATH"]


def main():
    for script in [SCHEMA_SCRIPTS + "\create_schema.sql", TABLE_SCIPTS + "\create_tables.sql"]:
        manipulation_database(script)

main()
