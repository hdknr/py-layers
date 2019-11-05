__version__ = '0.0.1'
import click
import pkgutil
import importlib
import sys


def dispatch():
    BASE = __name__
    if len(sys.argv) >= 2:
        name = sys.argv[1]
        try:
            mod = importlib.import_module(f"{BASE}.{name}")
            del sys.argv[1]
            getattr(mod, name)(obj={})
            return
        except:
            pass
