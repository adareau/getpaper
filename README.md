# getpaper

## description
getpaper is a small command-line tool writen in python to **get scientific papers from their references**. It uses the journals' search engine, automatically send to them a well formatted request, and scraps the answer (using BeautifulSoup) to get the paper url. If a paper is found, it opens its url on a new tab in the web browser. If there is an error, it opens the paper search page

## example

```bash
# general synthax :
# $> getpaper journal_name volume page
getpaper PRA 46 2668
getpaper Nature 519 211
getpaper arxiv 1706 07781
```

to get the list of implemented journal :

```bash
getpaper journals # returns list of journals

available journals : PRL, PRX, RMP, PRA, PRB, PRC, PRD, PRE, PR, Science, NatPhys, Nature, arxiv, arXiv, NJP, JPBold, JPB, OE, OL, AO, Optica
```
## limitations

So far, on top of broadband journals such as *Nature* or *Science* and the open-access *arXiv* repository, only a subset of **physics** journals is implemented.

**If you wish to contribute, by writing the code in a more elegant way or implementing new journals, do not hesitate to contact me.**

## notes

The script is written for **python 2.7**. It requires the installation of additionnal packages: 

-  [requests](https://pypi.python.org/pypi/requests): "*Python HTTP for Humans.*" Used to send requests to the journal's search engine and retrieve information.

- [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4/): "*Beautiful Soup sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.*" Used to parse the HTTP response.

For a simple install, I recommend using pip (https://pypi.python.org/pypi/pip/).
