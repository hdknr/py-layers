__version__ = '0.0.1'
import click
import pkgutil
import importlib
import sys


def dispatch():
    BASE = __name__
    func = None
    if len(sys.argv) >= 2:
        name = sys.argv[1]
        try:
            mod = importlib.import_module(f"{BASE}.{name}")
            del sys.argv[1]
            func = getattr(mod, name)
        except:
            pass

    func and func(obj={})