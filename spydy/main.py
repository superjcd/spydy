import os
import argparse
import configparser
import asyncio
from spydy import LOGO
from .engine import Engine
from .utils import check_configs_and_add_defaults
from .defaults import *


long_description = """
"""


def fire():
    print(LOGO)
    arg_parser = argparse.ArgumentParser(
        prog="spydy",
        description="High level spider framework for web crawling based on pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=long_description,
    )
    arg_parser.add_argument(
        "configfile",
        type=str,
        help="Please provide your configfile, then spydy will start soon.",
    )
    args = arg_parser.parse_args()
    configfile = args.configfile
    if not os.path.exists(configfile):
        raise FileExistsError("No such file: {!r}".format(configfile))

    config_parser = configparser.ConfigParser()
    config_parser.read(configfile, encoding="utf-8")
    check_configs_and_add_defaults(config_parser)
    engine = Engine.from_configparser(config_parser)
    engine.run()
