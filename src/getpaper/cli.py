#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File    : getpaper
Author  : A. Dareau

Comments: a small command-line tool to get papers from their references. It
          uses the journals' search engine, automatically send to them a well
          formatted request, and scraps the answer (using BeautifulSoup) to get
          the paper url. If a paper is found, it opens its url on a new tab in
          the web browser. If there is an error, it opens the paper search page

          Example :
              $> getpaper PRA 46 2668
              $> getpaper Nature 519 211
              $> getpaper arxiv 1706 07781
"""
# % Imports
import requests
import webbrowser
import sys

from bs4 import BeautifulSoup

# % Global Variables
# paper reference initialization
JOURNAL = "PRA"
ISSUE = "46"
PAGE = "2668"

# list of available journals
APS_NAMES_MATCH = {
    "PRL": "PhysRevLett",
    "PRX": "PhysRevX",
    "RMP": "RevModPhys",
    "PRA": "PhysRevA",
    "PRB": "PhysRevB",
    "PRC": "PhysRevC",
    "PRD": "PhysRevD",
    "PRE": "PhysRevE",
    "PRR": "PhysRevResearch",
    "PRApp": "PhysRevApplied",
    "PRXQuantum": "PRXQuantum",
}
APS_LIST = list(APS_NAMES_MATCH)
SCIENCE_LIST = ["Science"]
ARXIV_LIST = ["arxiv"]

NATURE_NAMES = {"Nature": "nature", "NatPhys": "nphys"}
NATURE_LIST = list(NATURE_NAMES.keys())

IOP_NAMES = {"JPBold": "0022-3700", "JPB": "0953-4075", "NJP": "1367-2630"}
IOP_LIST = list(IOP_NAMES.keys())

OSA_NAMES = {
    "OL": "ol",  # optics letters
    "OE": "oe",  # optics express
    "Optica": "optica",
    "AO": "ao",
}
OSA_LIST = list(OSA_NAMES.keys())

SCIPOST_PHYS_LIST = ["SPP", "SciPostPhys"]

ALL_JOURNALS = (
    APS_LIST
    + SCIENCE_LIST
    + NATURE_LIST
    + ARXIV_LIST
    + IOP_LIST
    + OSA_LIST
    + SCIPOST_PHYS_LIST
)

# OTHER VARIABLES
AUTOTEST = False

# % Help string

HELP_STRING = """
          a small command-line tool to get papers from their references. It
          uses the journals' search engine, automatically send to them a well
          formatted request, and scraps the answer (using BeautifulSoup) to get
          the paper url. If a paper is found, it opens its url on a new tab in
          the web browser. If there is an error, it opens the paper search page

          Example :
              $> getpaper PRA 46 2668
              $> getpaper Nature 519 211
              $> getpaper arxiv 1706 07781

          Get paper using DOI :
              $> getpaper doi 10.1103/physrevx.8.031054

          Other options :
              $> getpaper journals : returns implemented journal list
           """


# % Useful functions
def low_list(string_list):
    return [s.lower() for s in string_list]


def low_dict(dic):
    return {key.lower(): value for key, value in dic.items()}


# % Core functions
def start():
    """
    Will analyse input and act accordingly
    """
    global ALL_JOURNALS, HELP_STRING
    # if anything but "normal behaviour",do not go on
    go_on = False

    # -- wrong behaviour : no arguments or more than 3
    if len(sys.argv) == 1 or len(sys.argv) > 4:
        print(HELP_STRING)

    # -- special behaviour : only one argument
    elif len(sys.argv) == 2:
        option = sys.argv[1]
        if option.lower() == "journals":
            msg = "available journals : " + ", ".join(ALL_JOURNALS)
            print(msg)
        elif option.lower() == "autotest":
            autotest()
        else:
            print(HELP_STRING)

    # -- special behaviour : only two argument
    elif len(sys.argv) == 3:
        mode = sys.argv[1]
        option = sys.argv[2]
        if mode.lower() == "doi":
            get_DOI_reference(option)
        elif mode.lower() == "arxiv":
            # when calling "getpaper arxiv 1706.07781"
            # instead of "getpaper arxiv 1706 07781"
            get_arxiv_direct(option)
        else:
            print(HELP_STRING)

    # -- normal behaviour : three arguments
    elif len(sys.argv) == 4:
        go_on = True

    return go_on


def get_paper_properties():
    global JOURNAL, ISSUE, PAGE, ALL_JOURNALS
    # check number of inputs
    err_msg = "getpaper takes exactly 3 arguments : journal, issue, page"
    err_msg += "\n" + "example : getpaper PRA 46 2668"
    assert len(sys.argv) == 4, err_msg
    # get inputs
    JOURNAL, ISSUE, PAGE = sys.argv[1:]
    # check implemented journal
    err_msg = "%s is not an implemented journal" % JOURNAL
    err_msg += "\n" + "available journals : " + ", ".join(ALL_JOURNALS)
    JOURNAL = JOURNAL.lower()
    assert JOURNAL in low_list(ALL_JOURNALS), err_msg


def send_search_request():
    global JOURNAL, ISSUE, PAGE, APS_LIST, SCIENCE_LIST, NATURE_LIST, ARXIV_LIST, IOP_LIST, OSA_LIST, SCIPOST_PHYS_LIST, AUTOTEST
    # to be on the safe side
    JOURNAL = JOURNAL.lower()
    # get reference
    if JOURNAL in low_list(APS_LIST):
        url = get_APS_reference()
    elif JOURNAL in low_list(SCIENCE_LIST):
        url = get_Science_reference()
    elif JOURNAL in low_list(NATURE_LIST):
        url = get_Nature_reference()
    elif JOURNAL in low_list(ARXIV_LIST):
        url = get_arxiv_reference()
    elif JOURNAL in low_list(IOP_LIST):
        url = get_IOP_reference()
    elif JOURNAL in low_list(OSA_LIST):
        url = get_OSA_reference()
    elif JOURNAL in low_list(SCIPOST_PHYS_LIST):
        url = get_SciPostPhys_reference()
    else:
        url = "https://scholar.google.com/"
    # print url and go there
    print(" >>> going to %s" % url)
    if not AUTOTEST:
        webbrowser.open_new_tab(url)


# % Paper retrieval functions
def get_APS_reference():
    """
    The search server (https://journals.aps.org/search/citation) only takes
    posts requests (does not return anything otherwise). It directly sends us
    to the paper's page.
    """
    global JOURNAL, ISSUE, PAGE, APS_NAME_MATCH
    url = "https://doi.org/10.1103/{journal_key}.{issue}.{page}"
    journal_key = APS_NAMES_MATCH[JOURNAL.upper()]
    return url.format(journal_key=journal_key, issue=ISSUE, page=PAGE)


def get_Science_reference():
    """
    The search page is loaded dynamically, so I do not try to get
    the data from the page
    """
    global ISSUE, PAGE
    url = "https://www.science.org/action/doSearch"
    data = {
        "SeriesKey": "science",
        "quickLinkJournal": "science",
        "Volume": ISSUE,
        "FirstPage": PAGE,
    }
    params = [k + "=" + str(v) for k, v in data.items()]
    params = "&".join(params)
    url = url + "?" + params

    return url


def get_Nature_reference():
    """
    for Nature this is rather straightforward : the search server
    (https://www.nature.com/search) takes get requests. We scrap the
    first returned paper url looking for the 'search_result_rank_1' attribute.
    """
    global JOURNAL, ISSUE, PAGE, NATURE_NAMES
    url = "https://www.nature.com/search"
    names_dic = low_dict(NATURE_NAMES)
    data = {
        "journal": names_dic[JOURNAL],
        "order": "relevance",
        "volume": ISSUE,
        "spage": PAGE,
    }
    r = requests.get(url, params=data)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        attrs = {"itemprop": "url", "data-track-action": "view article"}
        url = soup.find("a", attrs=attrs)
        if url != None:
            url = url["href"]
            url = "https://www.nature.com%s" % url
        else:
            print("Error : paper not found")
            url = r.url
    else:
        print("Error : %i" % r.status_code)
        print(r.reason)
        url = r.url
    return url


def get_arxiv_reference():
    global JOURNAL, ISSUE, PAGE
    """
    this one is actually quite easy... I just include it for completeness
    """
    url = "https://arxiv.org/abs/%s.%s" % (ISSUE, PAGE)
    return url


def get_IOP_reference():
    global JOURNAL, ISSUE, PAGE, IOP_NAMES
    """
    for IOP papers we call the server (iopscience.iop.org/findcontent) with a
    simple get request. The journal name is coded (see list in source code of
    iopscience.iop.org/findcontent). A selection is implemented (in IOP_NAMES)
    """
    url = "http://iopscience.iop.org/findcontent"
    names_dic = low_dict(IOP_NAMES)
    data = {
        "CF_JOURNAL": names_dic[JOURNAL],
        "CF_VOLUME": ISSUE,
        "CF_ISSUE": "",
        "CF_PAGE": PAGE,
        "submit": "Go",
        "navsubmit": "Go",
    }
    r = requests.get(url, params=data)
    url = r.url
    return r.url


def get_OSA_reference():
    """
    for OSA papers we call the server (https://www.osapublishing.org/search.cfm)
    with a get request. Here the search page takes time to return a result, so
    we directly open it in the browser..
    #FIXME: find a way to wait for the result ?
    """
    global JOURNAL, ISSUE, PAGE, OSA_NAMES
    url = "https://www.osapublishing.org/search.cfm"
    names_dic = low_dict(OSA_NAMES)
    data = {"j": names_dic[JOURNAL], "q": "", "i": "", "v": ISSUE, "p": PAGE}

    params = [k + "=" + str(v) for k, v in data.items()]
    params = "&".join(params)
    url = url + "?" + params
    """
    r = requests.get(url, params = data, allow_redirects=True,
                     stream=True, timeout=None)
    """
    return url


def get_SciPostPhys_reference():
    """
    Scipost Physics reference
    """
    global JOURNAL, ISSUE, PAGE
    url = "https://scipost.org/search"
    data = {"q": "SciPost Phys %s %s" % (ISSUE, PAGE)}
    r = requests.get(url, params=data)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        attrs = {"class": "my-0"}
        paper = soup.find("h3", attrs=attrs)
        if paper != None:
            href = paper.a.attrs["href"]
            url = "https://scipost.org%s" % href
        else:
            print("Error : paper not found")
            url = r.url
        pass
    else:
        print("Error : %i" % r.status_code)
        print(r.reason)
        url = r.url
    return url


# % Other functions
def get_DOI_reference(doi):
    """
    this one is also quite easy
    """
    url = "https://doi.org/%s" % doi
    print(" >>> going to %s" % url)
    webbrowser.open_new_tab(url)


def get_arxiv_direct(ref):
    url = "https://arxiv.org/abs/%s" % ref
    print(" >>> going to %s" % url)
    webbrowser.open_new_tab(url)


def autotest():
    """
    auto test function
    """
    global JOURNAL, ISSUE, PAGE, AUTOTEST
    print("### Starting getpaper autotest")
    # set AUTOTEST to True : not opening sucessfull request in browser
    AUTOTEST = True
    # definitions
    paper_list = []
    paper_list.append(("PRL", "48", "596"))
    paper_list.append(("PRA", "5", "2217"))
    paper_list.append(("RMP", "40", "677"))
    paper_list.append(("arxiv", "1706", "07781"))
    paper_list.append(("Nature", "415", "39"))
    paper_list.append(("NatPhys", "1", "23"))
    paper_list.append(("NJP", "12", "033007"))
    paper_list.append(("OL", "21", "1777"))
    paper_list.append(("SciPostPhys", "5", "055"))
    # start test
    for paper in paper_list:
        JOURNAL, ISSUE, PAGE = paper
        print(" $> getpaper %s %s %s" % (JOURNAL, ISSUE, PAGE))
        send_search_request()
        print(" ")


# % Main
def app():
    if start():
        get_paper_properties()
        send_search_request()


# % Execute
if __name__ == "__main__":
    app()
