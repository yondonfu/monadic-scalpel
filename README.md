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

You also need to write your own parse function. You should write your parse function with the monadic find functions (`m_find`, `m_find_all`, `m_lst_get` and `m_dict_get`):

```python
from bs4 import BeautifulSoup
import lxml
from pymonad.Maybe import Just
from monadic_scalpel.parser import m_find, m_find_all, m_lst_get, m_dict_get

def parse_html(html):
    soup = BeautifulSoup(html, "lxml")

    return Just(soup) >> m_find_all("div", None, None) >> m_lst_get(0) >> m_find("a", None, None) >> m_dict_get("href")
```

You can pass the requester function and parse function to the scalp function:

```python
from monadic_scalpel.scalpel import scalp

scalp("http://streeteasy.com/for-sale/nyc", getter, parse_html)
```

