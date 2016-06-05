from bs4 import BeautifulSoup
import lxml

from pymonad.Maybe import Just
from pymonad.Reader import curry

from parser import m_find, m_find_all, m_lst_get, m_dict_get
from scalpel import scalp, make_getter

def parse_html(html):
    soup = BeautifulSoup(html, "lxml")
    
    # titles = Just(soup) >> m_find_all("div", "details-title", None)

    # return [title.a["href"] for title in titles.getValue()]
    res = Just(soup) >> m_find("div", "details", None) >> \
          m_find_all("div", "details_info", None) >> m_lst_get(1) >> \
          m_find_all("span", "nobreak", None) >> m_lst_get(1) >> \
          m_find("a", None, None) >> m_dict_get("href")

    return res

if __name__ == "__main__":
    getter = make_getter("proxies.txt", "ua.txt")
    # print scalp("http://streeteasy.com/for-sale/nyc", getter, parse_html)
    print scalp("http://streeteasy.com/building/trump-parc/7o?featured=1", \
                getter, parse_html)

