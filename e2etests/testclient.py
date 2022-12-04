"""
    Simple HTTP Client wrapper of python-requests package
"""

from functools import wraps
import inspect
import requests
from requests.compat import urljoin


class TestClient:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session(base_url=base_url)

    def get(self, *arg):
        return self.session.get(*arg)


# Wrapper functions to add base_url to request session
def _base_url(func, base):
    """
    Decorator for adding a base URL to func's url parameter
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        argname = 'url'
        argspec = inspect.getfullargspec(func)
        if argname in kwargs:
            kwargs[argname] = urljoin(base, kwargs[argname])
        else:
            for i, name in enumerate(argspec[0]):
                if name == argname:
                    args = list(args)
                    args[i-1] = urljoin(base, args[i-1])
                    break
        return func(*args, **kwargs)
    return wrapper


def inject_base_url(func):
    """
    Decorator for adding a base URL to all methods that take a url param
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        argname = 'base_url'
        if argname in kwargs:
            obj = args[0]
            # Add base_url decorator to all methods that have a url parameter
            for name, method in inspect.getmembers(obj, inspect.ismethod):
                argspec = inspect.getfullargspec(method.__func__)
                if 'url' in argspec[0]:
                    setattr(obj, name, _base_url(method, kwargs[argname]))
            del kwargs[argname]
        return func(*args, **kwargs)
    return wrapper


# Wrap requests.Session.__init__ so it takes a base_url parameter
setattr(requests.Session, '__init__', inject_base_url(getattr(requests.Session, '__init__')))