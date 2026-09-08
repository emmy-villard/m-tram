from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

def update_url_params(url, params):
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)