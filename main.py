import requests
from bs4 import BeautifulSoup


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


start('http://boards.4chan.org/tv/thread/90623217')
