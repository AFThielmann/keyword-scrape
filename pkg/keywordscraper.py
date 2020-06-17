import re
import webbot
import time
from bs4 import BeautifulSoup
import json
import numpy as np
import joblib

class KeyScraper:
    """
    Keywordscraper
    """

    def __init__(self):
        # define url - is already the result of search for the keyword "Artificial Intelligence"
        self.url = "https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22Author%20Keywords%22:Artificial%20Intelligence)"
        self.web = webbot.Browser()
        # define a delay function in order to prevent empty results when internet connection is slow
        self.delay = 3

    def open(self):
        # go to web page
        self.web.go_to(self.url)
        'wait'
        time.sleep(self.delay)
        # extend the displayed results to 100 paper
        #self.web.click("25")
        #time.sleep(self.delay)
        #self.web.click("100")
        time.sleep(self.delay)


    def find_links(self):
        document_links = []
        time.sleep(self.delay)
        # get html of source page
        html_page = self.web.get_page_source()

        soup = BeautifulSoup(html_page)

        # get the hyperlinks for all the documents and temporarily save them
        for link in soup.findAll('a', attrs={'href': re.compile("^/document")}):
            document_links.append(link.get('href'))

        # remove unnecessary results of the href search
        matching = [s for s in document_links if "citation" in s]

        self.data = [i for i in document_links if i not in matching]
        time.sleep(self.delay)


    def go_to_pages(self):
        time.sleep(self.delay)
        self.data = np.array(self.data)
        # remove duplicates that are in there due to multiple occurrence in the href
        self.data = np.unique(self.data)
        print(len(self.data))
        self.keys = []

        # go through every search result and do the following: open the keywords section,
        # extract the keywords (+ unnecessary stuff) ,append the keywords to self.keys
        for i in range(len(self.data)):

            self.web.go_to("https://ieeexplore.ieee.org" + self.data[i])
            time.sleep(self.delay)

            self.web.click('Keywords')
            time.sleep(self.delay)

            html_page = self.web.get_page_source()
            soup = BeautifulSoup(html_page)
            time.sleep(self.delay)

            # return class str
            for key in soup.findAll('a', attrs={"data-tealium_data": re.compile('')}):
                self.keys.append(key.get("data-tealium_data"))


    def get_keywords(self):

        temp = []
        # extract the keywords from dictionary like but class string data
        for i in range(3):
            temp.append(json.loads(self.keys[i]))
        self.keyword = []
        # extract the keywords
        for i in range(len(temp)):
            self.keyword.append(temp[i].get("keyword"))

        # remove all duplicates
        self.keyword = np.array(self.keyword)
        self.keyword = np.unique(self.keyword)
        self.keyword = self.keyword.tolist()
        print(len(self.keyword))

        # return the keywords for later saving
        return self.keyword


if __name__ == "__main__":

    # Execute the above code
    ks = KeyScraper()

    ks.open()
    ks.find_links()
    ks.go_to_pages()
    keywords = ks.get_keywords()
    # save the keyword list
    #joblib.dump(keywords, "keyword_list.pk")



