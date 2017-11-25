import requests
import dryscrape #for JS support
from bs4 import BeautifulSoup
from sqldb_creation import create_post, create_comment


def trade_spider(catalog_url, db_conn):
    session = dryscrape.Session()
    session.visit(catalog_url)
    response = session.body()
    soup = BeautifulSoup(response, "html.parser")
    for thread in soup.findAll('div', {'class': 'thread'}):
        post_title = thread.find('div', {'class': 'teaser'}).get_text()
        link = thread.find('a')['href']
        scrape_page('http:'+link, post_title, db_conn)


def scrape_page(url, post_title, conn):
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, "html.parser")
    post_div = soup.find('div', {'class': 'opContainer'})
    post = get_post(post_div)
    print(post)
    post_id = create_post(conn, post)
    print(post_id)
    for reply_div in soup.findAll('div', {'class': 'replyContainer'}):
        comment = get_reply(reply_div)
        if comment is "":
            continue
        comment = (post_id, comment[0], comment[1], comment[2])
        print(comment)
        create_comment(conn, comment)
    

def get_post(post_div):
    subject = post_div.find('span', {'class': 'subject'}).get_text()
    post_content = post_div.find('blockquote', {'class': 'postMessage'})
    post_text = get_text(post_content)
    if subject is not "":
        post_text = subject + ":\n" + post_text
    dateTime = post_div.find('span', {'class': 'dateTime'})
    for link in dateTime.findAll('a'):
        link.decompose()
    post_date = dateTime.get_text()
    post_date = post_date.strip()
    return (post_text, post_date, 0)


def get_reply(reply_div):
    content = reply_div.find('blockquote', {'class': 'postMessage'})
    reply_text = get_text(content)
    if reply_text is "":
        return ""
    dateTime = reply_div.find('span', {'class': 'dateTime'})
    for link in dateTime.findAll('a'):
        link.decompose()
    reply_date = dateTime.get_text()
    reply_date = reply_date.strip()
    return (reply_text, reply_date, 0)


def get_text(soup):
    for link in soup.findAll('a', {'class': 'quotelink'}):
        link.decompose()
    for br in soup.findAll('br'):
        br.replace_with("\n")
    text = soup.get_text()
    text = text.strip()
    return text


