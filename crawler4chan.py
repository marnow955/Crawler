import requests
import dryscrape #for JS support
from bs4 import BeautifulSoup


def trade_spider(catalog_url):
    session = dryscrape.Session()
    session.visit(catalog_url)
    response = session.body()
    soup = BeautifulSoup(response, "html.parser")
    for thread in soup.findAll('div', {'class': 'thread'}):
        post_title = thread.find('div', {'class': 'teaser'}).get_text()
        print(post_title)
        link = thread.find('a')['href']
        print(link)
        scrape_page('http:'+link, post_title)


def scrape_page(url, post_title):
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
        if content == post_title:
            continue
        print(content)
