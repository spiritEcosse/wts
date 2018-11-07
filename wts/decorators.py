from functools import wraps

from bs4 import BeautifulSoup


def check_base(tags, class_):
    def decorator(func):
        @wraps(func)
        def func(*args, **kwargs):
            html = args[1]
            soup = BeautifulSoup(html, "html.parser")
            return all((soup.contents[0].name in tags, class_ in html))
        return func
    return decorator
