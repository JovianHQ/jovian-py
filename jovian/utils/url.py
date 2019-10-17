def urljoin(*args):
    """Join multiple url parts to construct one url"""
    if len(args) == 0:
        raise TypeError("urljoin requires at least one argument")

    trailing_slash = '/' if args[-1].endswith('/') else ''

    return '/'.join(map(lambda x: str(x).strip('/'), args)) + trailing_slash
