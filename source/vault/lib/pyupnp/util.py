import urlparse

__author__ = 'Dean Gardiner'


def http_parse_raw(data):
    lines = data.split('\r\n')

    version, respCode, respText = None, None, None
    headers = {}

    for x in range(len(lines)):
        if x == 0:
            version, respCode, respText = lines[0].split()
            respCode = int(respCode)
        elif x > 0 and lines[x].strip() != '':
            sep = lines[x].index(':')
            hk = lines[x][:sep].lower()
            hv = lines[x][sep+1:].strip()

            if headers.has_key(hk):
                headers[hk] = [headers[hk], hv]
            else:
                headers[hk] = hv

    return version, respCode, respText, headers


def absolute_url(baseUrl, url):
    if url.strip() == '':
        return url

    urlp = urlparse.urlparse(url)
    if urlp.netloc == '':
        url = urlparse.urljoin(baseUrl, url)

    return url