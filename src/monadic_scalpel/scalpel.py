import requests
from pymonad.Reader import curry
from lib.rotator import make_rotator, read_file

def make_scalpel(method, parse_func, proxy_file, ua_file):
    proxies = make_rotator(read_file(proxy_file))
    ua = make_rotator(read_file(ua_file))

    # Compose parse and data functions
    # Data function applied first, then result is passed to parse function
    if method == "GET":
        scalpel = parse_func * get_data
    else:
        scalpel = parse_func * post_data

    # Return partially applied scalpel function with
    # proxy and ua rotators
    return scalpel(proxies, ua)

@curry
def get_data(proxies, ua, url, params=None):
    @timeout
    def get(proxy, agent, url, params=None):
        proxy = {"http": "http://" + proxy}
        headers = {"User-Agent": agent}

        r = requests.get(url, proxies=proxy, headers=headers)

        return r.text

    retries = 0

    while get(proxies.next(), ua.next(), url, params) == Nothing):
        if retries <= MAX_RETRIES:
            return Nothing
        
        retries += 1
    
@curry
def post_data(proxies, ua, url, params=None):
    proxy = {"http": "http://" + proxies.next()}
    headers = {"User-Agent": ua.next()}

    r = requests.post(url, proxies=proxy, headers=headers)

    return r.text




