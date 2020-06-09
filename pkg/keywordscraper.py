import re
import webbot
import time
from bs4 import BeautifulSoup
import json

class KeyScraper:
    """
    Keywordscraper
    """

    def __init__(self):
        self.url = "https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22Author%20Keywords%22:Artificial%20Intelligence)"
        self.web = webbot.Browser()
        self.delay = 3

    def open(self):
        self.web.go_to(self.url)
        time.sleep(self.delay)


    def find_links(self):
        document_links = []
        time.sleep(self.delay)
        html_page = self.web.get_page_source()

        soup = BeautifulSoup(html_page)

        for link in soup.findAll('a', attrs={'href': re.compile("^/document")}):
            document_links.append(link.get('href'))

        matching = [s for s in document_links if "citation" in s]

        self.data = [i for i in document_links if i not in matching]
        time.sleep(self.delay)


    def go_to_pages(self):
        time.sleep(self.delay)
        self.web.go_to("https://ieeexplore.ieee.org" + self.data[0])
        time.sleep(self.delay)
        self.web.click('Keywords')
        time.sleep(self.delay)


    def get_keywords(self):
        html_page = self.web.get_page_source()
        soup = BeautifulSoup(html_page)
        time.sleep(self.delay)
        keys = []
        time.sleep(self.delay)
        for key in soup.findAll('a', attrs={"data-tealium_data": re.compile('')}):
            keys.append(key.get("data-tealium_data"))
        print(keys[0])
        temp = []
        for i in range(len(keys)):
            temp.append(json.loads(keys[i]))
        self.keyword = []
        for i in range(len(temp)):
            self.keyword.append(temp[i].get("keyword"))
        print(self.keyword)

        #for key in soup.findAll('a', attrs={'class': re.compile("^keywords")}):
        #    keywords.append(key.get('class'))
        #print(keywords)



if __name__ == "__main__":
    ks = KeyScraper()

    ks.open()
    ks.find_links()
    ks.go_to_pages()
    ks.get_keywords()


