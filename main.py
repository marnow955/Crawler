import requests
from bs4 import BeautifulSoup
from sqldb_creation import *
from crawler4chan import *


def main():
    database = "posts.db"

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

    
    url = "http://boards.4chan.org/tv/catalog"

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_posts_table)
        create_table(conn, sql_create_comments_table)
    else:
        print("Error! cannot create the database connection.")
    
    trade_spider(url)


if __name__ == '__main__':
    main()


def start(url):
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, "html.parser")
    for post_text in soup.findAll('blockquote', {'class': 'postMessage'}):
        for link in soup.findAll('a', {'class': 'quotelink'}):
            link.decompose()
        for br in soup.find_all("br"):
            br.replace_with("\n")
        content = post_text.get_text()
        content = content.strip()
        if content is "":
            continue
        print(content)


#start('http://boards.4chan.org/tv/thread/90623217')

# http://boards.4chan.org/tv/catalog
# dopóki counter postów mniejszy od zakładanej wartości to odwiedzaj kolejne tablice i pobieraj posty
