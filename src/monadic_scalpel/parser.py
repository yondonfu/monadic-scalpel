from pymonad.Maybe import *
from pymonad.Reader import curry
from bs4 import ResultSet, Tag
import lxml

@curry
def m_find(tag, tag_cls, tag_id, soup):
    if soup is None:
        return Nothing

    if tag_cls:
        return Just(soup.find(tag, {"class": tag_cls}))
    elif tag_id:
        return Just(soup.find(tag, {"id": tag_id}))
    else:
        return Just(soup.find(tag))

@curry
def m_find_all(tag, tag_cls, tag_id, soup):
    if soup is None:
        return Nothing

    if tag_cls:
        return Just(soup.find_all(tag, {"class": tag_cls}))
    elif tag_id:
        return Just(soup.find_all(tag, {"id": tag_id}))
    else:
        return Just(soup.find_all(tag))

@curry
def m_lst_get(idx, soup):
    if soup is None:
        return Nothing

    if type(soup) is not ResultSet or len(soup) <= idx:
        return Nothing

    return Just(soup[idx])

@curry
def m_dict_get(key, soup):
    if soup is None:
        return Nothing

    if type(soup) is not Tag:
        return Nothing

    return Just(soup[key])
