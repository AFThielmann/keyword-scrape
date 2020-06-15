import re
import webbot
import time
from bs4 import BeautifulSoup
import json
import numpy as np
import joblib
import pandas as pd

def RemoveInList(sub,LinSplitUnOr):
    indices = [i for i, x in enumerate(LinSplitUnOr) if re.search(sub, x)]
    A = [i for j, i in enumerate(LinSplitUnOr) if j not in indices]
    return A

sub = " Abstract:\n"

class AbstractScraper:
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
        time.sleep(self.delay)
        # get html of source page
        self.html_page = []
        self.html_page.append(self.web.get_page_source())
        time.sleep(self.delay)
        time.sleep(self.delay)
        self.web.click("Next")
        time.sleep(self.delay)
        self.html_page.append(self.web.get_page_source())

        time.sleep(self.delay)
        self.web.click("Next")
        time.sleep(self.delay)
        self.html_page.append(self.web.get_page_source())
        time.sleep(self.delay)
        time.sleep(self.delay)
        time.sleep(self.delay)
        self.web.click("Next")
        time.sleep(self.delay)
        self.html_page.append(self.web.get_page_source())
        time.sleep(self.delay)
        time.sleep(self.delay)
        time.sleep(self.delay)
        self.web.click("Next")
        time.sleep(self.delay)
        self.html_page.append(self.web.get_page_source())
        time.sleep(self.delay)
        time.sleep(self.delay)
        time.sleep(self.delay)
        self.web.click("Next")
        time.sleep(self.delay)
        self.html_page.append(self.web.get_page_source())
        time.sleep(self.delay)

        print(len(self.html_page))
        return self.html_page


    def find_links(self):

        self.data = []
        for j in range(2):#len(self.html_page)):
            soup = BeautifulSoup(self.html_page[j])
            document_links = []
            # get the hyperlinks for all the documents and temporarily save them
            for link in soup.findAll('a', attrs={'href': re.compile("^/document")}):
                document_links.append(link.get('href'))

        # remove unnecessary results of the href search
            matching = [s for s in document_links if "citation" in s]


            x = [i for i in document_links if i not in matching]
            self.data.append(x)
            time.sleep(self.delay)

            time.sleep(self.delay)
        self.data = np.array(self.data)
            # remove duplicates that are in there due to multiple occurrence in the href
        self.data = np.unique(self.data)
        print(len(self.data))
        return self.data


    def get_abstracts(self):

        self.abstracts = []

        # go through every search result and do the following: open the keywords section,
        # extract the keywords (+ unnecessary stuff) ,append the keywords to self.keys
        for i in range(len(self.data)):#len(self.data)):

            self.web.go_to("https://ieeexplore.ieee.org" + self.data[i])
            time.sleep(self.delay)

            html_page = self.web.get_page_source()
            soup = BeautifulSoup(html_page)
            time.sleep(self.delay)

            texts = soup.find_all('div', {"class": "u-mb-1"})
            for t in texts:
                text = t.text.strip()
                text = text.replace('Abstract:\n', ' ')
                df_dict = {'text': text}
            self.abstracts.append(df_dict)

        return pd.DataFrame(self.abstracts)




if __name__ == "__main__":

    # Execute the above code
    ks = AbstractScraper()

    x = ks.open()
    y = ks.find_links()
    data = ks.get_abstracts()

    # save the keyword list
    #joblib.dump(keywords, "keyword_list.pk")



