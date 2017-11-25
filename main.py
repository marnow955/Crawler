import requests
from bs4 import BeautifulSoup
from sqldb_creation import *
from crawler4chan import *


def main():
    database = "posts.db"
    url = "http://boards.4chan.org/tv/catalog"

    sql_create_posts_table = """ CREATE TABLE IF NOT EXISTS posts (
                                     post_id integer primary key autoincrement,
                                     content text not null,
                                     date text not null,
                                     flag integer not null
                                 );"""    


    sql_create_comments_table = """ CREATE TABLE IF NOT EXISTS comments (
                                        com_id integer primary key autoincrement,
                                        parent_id integer not null,
                                        content text not null,
                                        date text not null,
                                        flag integer not null,
                                        FOREIGN KEY(parent_id) REFERENCES posts(post_id)
                                    );"""

    

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_posts_table)
        create_table(conn, sql_create_comments_table)
    else:
        print("Error! cannot create the database connection.")
    
    trade_spider(url, conn)
    close_connection(conn)


if __name__ == '__main__':
    main()



