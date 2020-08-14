import re
import webbot
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


sub = " Abstract:\n"


class AbstractScraper:
    """
    Keywordscraper
    """

    def __init__(self):
        # define url - is already the result of search for the keyword
        # "Artificial Intelligence"
        self.url = "https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=Machine%20Learning&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&rowsPerPage=100&pageNumber=1"
        self.web = webbot.Browser()
        # define a delay and wait function in order to prevent empty results
        # when internet connection is slow
        self.delay = 3
        self.wait = 7

    def open(self):
        # go to web page
        self.web.go_to(self.url)

        time.sleep(self.delay)
        self.html_page = []
        self.html_page.append(self.web.get_page_source())

        time.sleep(self.wait)

        for i in range(2, 15):
            time.sleep(self.wait)
            self.web.click(str(i))
            time.sleep(self.wait)
            self.html_page.append(self.web.get_page_source())

        print(len(self.html_page))
        return self.html_page

    def find_links(self):
        document_links = []
        self.data = []
        for j in range(len(self.html_page)):
            soup = BeautifulSoup(self.html_page[j])
            time.sleep(self.wait)

            # get the hyperlinks for all the documents and temporarily save
            # them
            for link in BeautifulSoup(self.html_page[j]).findAll(
                "a", attrs={"href": re.compile("^/document")}
            ):
                document_links.append(link.get("href"))
            time.sleep(self.wait)

        # remove unnecessary results of the href search
        matching = [s for s in document_links if "citation" in s]
        x = [i for i in document_links if i not in matching]
        self.data = x
        time.sleep(self.wait)

        self.data = np.array(self.data)
        # remove duplicates that are in there due to multiple occurrence in the
        # href
        self.data = np.unique(self.data)
        print(len(self.data))
        return self.data

    def get_abstracts(self):

        self.abstracts = []

        # go through every search result and do the following: open the keywords section,
        # extract the keywords (+ unnecessary stuff) ,append the keywords to
        # self.keys
        for i in range(len(self.data)):

            self.web.go_to("https://ieeexplore.ieee.org" + self.data[i])
            time.sleep(self.delay)

            html_page = self.web.get_page_source()
            soup = BeautifulSoup(html_page)
            time.sleep(self.delay)

            texts = soup.find_all("div", {"class": "u-mb-1"})
            for t in texts:
                text = t.text.strip()
                text = text.replace("Abstract:\n", " ")
                df_dict = {"text": text}
            self.abstracts.append(df_dict)

        return pd.DataFrame(self.abstracts)


if __name__ == "__main__":

    # Execute the above code
    ks = AbstractScraper()

    html_code = ks.open()
    links = ks.find_links()
    abstracts = ks.get_abstracts()

    abstracts.to_csv("ai_machine_deep.txt", header=True, index=False)
