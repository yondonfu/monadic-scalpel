import requests
from pymonad.Reader import curry
from pymonad.Maybe import Just, Nothing
from lib.rotator import make_rotator, read_file

MAX_RETRIES = 3 # Max number of request retries
TIMEOUT = 10 # Request timeout value

def scalp(url, requester, parse_func, requester_params=None):
    """
    Request url and parse response
    Accepts a requester function and a parse function as parameters
    """
    retries = 0
    
    while retries < MAX_RETRIES:
        resp = requester(url, requester_params)

        if resp != Nothing:
            # Parse response upon successful request
            return parse_func(resp.getValue())

        retries += 1

    # Exceeded max number of retries - use Nothing to represent failed operation
    return Nothing

# Requesters

def make_getter(proxy_file, ua_file, https=False):
    """
    Create a get requester
    """
    proxies = make_rotator(read_file(proxy_file))
    ua = make_rotator(read_file(ua_file))

    def get(url, params=None):
        """
        Local get function to handle request operation
        """
        if https:
            proxy = {"https": "https://" + proxies.next()}
        else:
            proxy = {"http": "http://" + proxies.next()}
            
        headers = {"User-Agent": ua.next()}

        try:
            r = requests.get(url, proxies=proxy, headers=headers, params=params, timeout=TIMEOUT)
        except: # Catch all exceptions and return Nothing
            # Can log type of exception here
            return Nothing
        else:
            return Just(r.text)

    return get # Closure closes over the proxy and ua rotators

def make_poster(proxy_file, ua_file, https=False):
    """
    Create a post requester
    """
    proxies = make_rotator(read_file(proxy_file))
    ua = make_rotator(read_file(ua_file))

    def post(url, params=None):
        """
        Local post function to handle request operation
        """
        if https:
            proxy = {"https": "https://" + proxies.next()}
        else:
            proxy = {"http": "http://" + proxies.next()}
            
        headers = {"User-Agent": ua.next()}

        try:
            r = requests.post(url, proxies=proxy, headers=headers, data=params, timeout=TIMEOUT)
        except: # Catch all exceptions and return Nothing
            # Can log type of exception here
            return Nothing
        else:
            return Just(r.text)

    return post # Closure closes over the proxy and ua rotators




