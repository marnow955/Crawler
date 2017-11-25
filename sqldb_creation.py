from sqlite3 import *


def create_connection(db_file):
    try:
        conn = connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def close_connection(conn):
    conn.close()


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

