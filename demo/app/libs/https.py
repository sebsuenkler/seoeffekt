from urllib.parse import urlparse

def check_https(url):
    #check https
    https = 0
    parsed = urlparse(url)
    scheme = parsed.scheme

    if scheme == 'https':
        https = 1

    return https
