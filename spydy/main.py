import os
import argparse
import configparser
import asyncio
from .engine import Engine
from .utils import configs_assertion
from .defaults import *


def fire():
    arg_parser = argparse.ArgumentParser()
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
    configs_assertion(config_parser)
    engine = Engine(config_parser)

    run_mode = config_parser["Globals"].get("run_mode", RUNMODE)
    engine.run(run_mode)


def _fire_for_test(configfile):
    config_parser = configparser.ConfigParser()
    config_parser.read(configfile, encoding="utf-8")
    configs_assertion(config_parser)
    engine = Engine(config_parser)

    run_mode = config_parser["Globals"].get(
        "run_mode", RUNMODE
    )  # choose run mode: once, forever, async:
    if run_mode == "once":
        engine.run_once()
    if run_mode == "forever":
        engine.run_forever()
    if run_mode == "async":
        nworkers = int(config_parser["Globals"].get("nworkers", NWORKERS))
        loop = asyncio.get_event_loop()
        engine.run_async(loop, nworkers)
