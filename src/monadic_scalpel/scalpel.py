import requests
from pymonad.Reader import curry
from pymonad.Maybe import Just, Nothing
from lib.rotator import make_rotator, read_file
from lib.timeout import timeout

MAX_RETRIES = 3 # Max number of request retries
TIMEOUT = 10 # Request timeout value

def scalp(url, requester, parse_func, requester_params=None):
    retries = 0

    while retries < MAX_RETRIES:
        print "Trying"
        res = requester(url, requester_params)

        if res != Nothing:
            return parse_func(res.getValue())

        retries += 1

    return Nothing

def make_getter(proxy_file, ua_file):
    proxies = make_rotator(read_file(proxy_file))
    ua = make_rotator(read_file(ua_file))

    def get(url, params=None):
        proxy = {"http": "http://hiro0:snowcrash@" + proxies.next()}
        headers = {"User-Agent": ua.next()}

        try:
            r = requests.get(url, proxies=proxy, headers=headers, params=params, timeout=TIMEOUT)
        except: # Catch all exceptions and return Nothing
            # Can log type of exception here
            return Nothing
        else:
            return Just(r.text)
            
    return get

def make_poster(proxy_fiile, ua_file):
    proxies = make_rotator(read_file(proxy_file))
    ua = make_rotator(read_file(ua_file))

    def post(url, params=None):
        proxy = {"http": "http://hiro0:snowcrash@" + proxies.next()}
        headers = {"User-Agent": ua.next()}

        try:
            r = requests.post(url, proxies=proxy, headers=headers, data=params)
        except: # Catch all exceptions and return Nothing
            # Can log type of exception here
            return Nothing
        else:
            return Just(r.text)

    return post




