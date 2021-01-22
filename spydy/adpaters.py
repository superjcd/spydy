def url_for_request(url):
    if isinstance(url, str):
        return url
    elif isinstance(url, bytes):
        return url.decode("utf-8")
    else:
        raise TypeError("Url type of <{}> is not supported yet".format(type(url)))
