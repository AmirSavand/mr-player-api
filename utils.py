from urllib.parse import urlparse, parse_qs

YOUTUBE_DOMAINS = [
    'youtu.be',
    'youtube.com',
]


def get_youtube_id(url_string: str):
    # Make sure all the URL start with a valid scheme
    if not url_string.lower().startswith('http'):
        url_string = 'http://%s' % url_string

    # Parse the URL
    url = urlparse(url_string)

    # Check host against whitelist of domains
    if url.hostname.replace('www.', '') not in YOUTUBE_DOMAINS:
        return None

    # Video ID is usually to be found in 'v' query string
    qs = parse_qs(url.query)
    if 'v' in qs:
        return qs['v'][0]

    # Otherwise fall back to path component
    return url.path.lstrip('/')
