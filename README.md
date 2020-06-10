# Paper Keyword scrape

The goal is, to get relevant keywords that appear in conjunction with artifial intelligence.

Opens the page https://ieeexplore.ieee.org/Xplore/home.jsp, or to prespecified search results on IEEExplore. The chosen search is "Artifial Intelligence" in "Author-Keywords". 

keywordscraper.py iterates through 100 search results (could be increased) and scrape all the Keywords of the found papers. All duplicates are removed and the keyword-list for further categorizing AI is saved.
