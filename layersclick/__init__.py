__version__ = "0.0.1"


def subcommands():
    import glob
    import os

    return [
        os.path.basename(i).replace(".py", "")
        for i in glob.glob(os.path.dirname(__file__) + "/*.py")
        if i.find("__init__.py") < 0
    ]


def get_subcommand():
    import argparse

    parser = argparse.ArgumentParser(
        description="AWS Command Tools Set", add_help=False)
    parser.add_argument("subcommand", choices=subcommands())
    args, unkonwns = parser.parse_known_args()
    return args.subcommand


def dispatch():
    import importlib
    import sys

    BASE = __name__
    func = None
    if len(sys.argv) >= 2:
        name = get_subcommand()
        try:
            mod = importlib.import_module(f"{BASE}.{name}")
            del sys.argv[1]
            func = getattr(mod, name)
        except Exception:
            import traceback

            print(traceback.format_exc())
            pass

    func and func(obj={})
