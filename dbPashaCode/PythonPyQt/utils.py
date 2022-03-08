import os
import sys
from io import StringIO
from time import time
from functools import wraps

import pandas as pd
import yaml
import psycopg2
from psycopg2 import extras
from psycopg2 import OperationalError

CURRENT_DIR = os.getcwd()


def get_yaml_conf(settings_filename):
    with open(settings_filename, "r") as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
    return settings


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print("func: {} took: {} sec".format(f.__name__, round(te - ts)))
        return result

    return wrap


class Configuration(object):
    _instance = None
    _d = {}

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            Configuration._instance = object.__new__(Configuration, *args, **kwargs)
            settings = get_yaml_conf(os.environ['CONFIG_PATH'])
            Configuration._instance.store_dict(settings)
            if "POSTGRES" in settings.keys():
                if sys.platform == "win32":
                    if "CREDENTIALS_PATH_WIN32" in settings["POSTGRES"]:
                        account_settings = get_yaml_conf(CURRENT_DIR + settings["POSTGRES"]["CREDENTIALS_PATH_WIN32"])
                        Configuration._instance._d["POSTGRES"].update(account_settings)
                    else:
                        if "CREDENTIALS_PATH_LINUX" in settings["POSTGRES"]:
                            account_settings = get_yaml_conf(
                                CURRENT_DIR + settings["POSTGRES"]["CREDENTIALS_PATH_LINUX"])
                            Configuration._instance._d["POSTGRES"].update(account_settings)
        return class_._instance

    def store_dict(self, d):
        for key, value in d.items():
            if not (key in self._d and value is None):
                self._d[key] = value

    def __setitem__(self, key, value):
        self._d[key] = value

    def __getitem__(self, key):
        return self._d[key]

    def __contains__(self, key):
        return key in self._d


def get_postgres_connection():
    postgres_conf = Configuration()["POSTGRES"]

    hostname = postgres_conf['host']
    login = postgres_conf['login']
    database = postgres_conf['database']
    password = postgres_conf['password']

    print(
        "Postgres connection: HOSTNAME {}, LOGIN {}, DATABASE {}".format(hostname, login, database))

    try:
        conn = psycopg2.connect(
            dbname=database,
            user=login,
            host=hostname,
            password=password,
        )
    except Exception as e:
        print("Something gone wrong", e)
        raise
    return conn


@timing
def load_from_postgres_filename(filename, conn):
    with open(filename, "r") as file:
        sql = file.read()
    ans = pd.read_sql(sql, conn)
    return ans


@timing
def load_from_postgres_query(query):
    conn = get_postgres_connection()
    try:
        ans = pd.read_sql(query, conn)
    except pd.io.sql.DatabaseError as e:
        print(e)
    return ans


@timing
def load_to_postgres(conn, df, table):
    print("start copy dataframe to Postgres {}".format(table))
    buffer = StringIO()
    df.to_csv(buffer, header=False)
    buffer.seek(0)

    cur = conn.cursor()
    try:
        df_columns = list(df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)

        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

        # create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO {} ({}) {}".format(table, columns, values)

        cur = conn.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt, df.values)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print("Something gone wrong", e)
        conn.rollback()
        cur.close()
    print("finish copy dataframe to Postgres {}".format(table))
    cur.close()


def is_table_exists(tablename: str):
    conn = get_postgres_connection()
    query = f"""
        SELECT * FROM {tablename} LIMIT 1;
    """
    try:
        pd.read_sql(query, conn)
    except pd.io.sql.DatabaseError as e:
         print(e)
         return False
    finally:
        conn.close()
    return True


def manipulation_database(script_filename: str):
    con = get_postgres_connection()
    con.autocommit = True
    cursor = con.cursor()
    try:
        cursor.execute(open(script_filename, "r").read())
        print("{}".format(script_filename))
    except OperationalError as e:
        print("Something gone wrong", e)


def get_data_function(nuclide: int, tablename: str):
    if is_table_exists(tablename):
        query = f"""
            SELECT *
            FROM {tablename}
            WHERE 'nuclide' = {nuclide}
        """
        ans = load_from_postgres_query(query)
    else:
        return None
    return ans