from sqlite3 import *


def create_connection(db_file):
    try:
        conn = connect(db_file, isolation_level=None)
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


def create_post(conn, post):
    sql = ''' INSERT INTO posts(content, date, flag) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, post)
    return cur.lastrowid


def create_comment(conn, comment):
    sql = ''' INSERT INTO comments(parent_id, content, date, flag) 
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, comment)
    return cur.lastrowid


