# Monadic Scalpel

Monadic Scalpel is a Python web scraping library using monadic programming built on [requests](http://docs.python-requests.org/en/master/),
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and [PyMonad](https://pypi.python.org/pypi/PyMonad/). 

## Installation

Clone this repository and navigate into the top directory

```python
python setup.py install
```

## Quickstart

To request and parse a URL you first need a requester function:

```python
from monadic_scalpel.scalpel import make_getter

getter = make_getter("proxies.txt", "ua.txt")
```

The requester functions created by `make_getter` and `make_poster` accept a file with a list of proxies and a file with a list of user agents as parameters. The requester functions will rotate through proxies and user agents as they are called. The requester functions also have a retry mechanism such that if a request operation fails, the function will retry for a certain number of times before giving up.

Note: If a proxy has a username and password each line of the proxy file should be in the format username:password@proxyip. For the user agent file each line should be the user agent string (not enclosed in quotes).

There are open web proxy lists available online such as [InCloak](https://incloak.com/proxy-list/) or [HMA](https://www.hidemyass.com/proxy). These resources can be an initial resource but for more secure and faster proxies you can buy them online from a service.

You also need to write your own parse function. You should write your parse function with the monadic parser functions (`m_find`, `m_find_all`, `m_lst_get` and `m_dict_get`) and PyMonad's monadic operator >> which allows you to create a data pipeline in your parse function.

```python
from bs4 import BeautifulSoup
import lxml
from pymonad.Maybe import Just
from monadic_scalpel.parser import m_find, m_find_all, m_lst_get, m_dict_get

def parse_html(html):
    soup = BeautifulSoup(html, "lxml")

    return Just(soup) >> m_find_all("div", None, None) >> m_lst_get(0) >> m_find("a", None, None) >> m_dict_get("href")
```

The monadic parser functions are curried using PyMonad's curry decorator. This allows you to use PyMonad's monadic operator >> to propagate data down the pipeline applying the curried monadic functions on the data at each step. If at any point in the pipeline a parsing operation fails, Nothing will be returned and propagated down the pipeline thereby avoiding any exceptions that could break your scraper. A future step would be to include logging such that you can see a more detailed error message in a log while still being able to avoid breaking your scraper.

You can pass the requester function and parse function to the scalp function:

```python
from monadic_scalpel.scalpel import scalp

scalp("http://streeteasy.com/for-sale/nyc", getter, parse_html)
```

Example of a scraper written with monadic scalpel:

```python
from monadic_scalpel.scalpel import make_getter, scalp
from monadic_scalpel.parser import m_find, m_find_all, m_lst_get, m_dict_get
from pymonad.Maybe import Just
from bs4 import BeautifulSoup
import lxml

def parse_html(html):
    soup = BeautifulSoup(html, "lxml")

    return Just(soup) >> m_find("div", "in_this_building big_separator", None) >> m_find_all("div", "details_info", None) >> \
        m_lst_get(0) >> m_find("a", None, None) >> m_dict_get("href")

if __name__ == "__main__":
    getter = make_getter("proxies.txt", "ua.txt")

    print scalp("http://streeteasy.com/building/203-west-137-street-manhattan/1?featured=1", getter, parse_html)
```


