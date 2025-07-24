# pip install mysql-connector-python
import mysql.connector
import utils
import json

cfg_file = open("sql.json")
config = json.loads(cfg_file.read())
cfg_file.close()
disable = config["disable"]

cnx = mysql.connector.connect(
    user="root", password="", host="127.0.0.1", database="krishna_life"
)

if not (cnx and cnx.is_connected()):
    utils.error("Failed to connect to DB, Haribol!")


def query(qry: str):
    try:
        with cnx.cursor() as cursor:
            cursor.execute(qry)
            cursor.fetchone()
            return True
    except:
        return False


def check_table(name):
    check_column(name, "*")


def check_column(table, column):
    if disable:
        return
    if not query(f"SELECT {column} from {table} LIMIT 1"):
        if column == "*":
            utils.error(f"Table {table} seems to be missing, Haribol.")
        else:
            utils.error(f"Column {column} in {table} seems to be missing, Haribol.")
