import mysql.connector
import utils


cnx = mysql.connector.connect(
    user="root", password="", host="127.0.0.1", database="krishna_life"
)

if not (cnx and cnx.is_connected()):
    utils.error("DB connection failure, Haribol!")


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
    if not query(f"SELECT {column} from {table} LIMIT 1"):
        if column == "*":
            utils.error(f"Table {table} seems to be missing, Haribol.")
        else:
            utils.error(f"Column {column} in {table} seems to be missing, Haribol.")
