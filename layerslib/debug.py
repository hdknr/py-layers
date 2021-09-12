import logging
import os
import sys

import pkg_resources


def info():
    data = {}
    data["syspath"] = sys.path
    data["pkg_resources"] = sorted(
        f"{p.project_name} {p.parsed_version} {p.location}" for p in pkg_resources.working_set
    )
    return data


def getLogger(level=None):
    level = level or os.environ.get("LOGLEVEL", logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(level)
    return logger
