import mysql.connector
from utils import *


def query(qry: str):
    cnx = mysql.connector.connect(
        user="root", password="", host="127.0.0.1", database="krishna_life"
    )

    if cnx and cnx.is_connected():
        try:
            with cnx.cursor() as cursor:
                cursor.execute(qry)
                cursor.fetchone()
                return True
        except:
            return False
        finally:
            cnx.close()
    else:
        raise Exception("Failed to connect to the DB, Haribol!")


def check_table(name):
    if not query(f"SELECT * from {name} LIMIT 1"):
        error(f"Table {name} seems to be missing, Haribol.")


def check_column(table, column):
    if not query(f"SELECT {column} from {table} LIMIT 1"):
        error(f"Column {column} in {table} seems to be missing, Haribol.")
