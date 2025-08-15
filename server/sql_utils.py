# pip install mysql-connector-python
import mysql.connector
import utils
from config import connect, config

check_db = config["check_db"]
# connect = config["connect"]

if check_db:
    cnx = mysql.connector.connect(
        user=connect["user"],
        password=connect["password"],
        host=connect["host"],
        database=connect["database"],
    )

    if not (cnx and cnx.is_connected()):
        utils.error("Failed to connect to DB, Haribol!")


def _query(qry: str):
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
    if not check_db:
        return
    if not _query(f"SELECT {column} from {table} LIMIT 1"):
        if column == "*":
            utils.error(f"Table {table} seems to be missing, Haribol.")
        else:
            utils.error(f"Column {column} in {table} seems to be missing, Haribol.")
