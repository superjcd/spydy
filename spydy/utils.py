from datetime import datetime
from typing import List
from functools import reduce
from reprlib import repr
import importlib
import sys
import spydy
from spydy.urls import Urls
from spydy.defaults import RUNMODES
from spydy.adpaters import url_for_request
from spydy.exceptions import UrlsStepNotFound


def class_dispatcher(user_provide_classname: str):
    if user_provide_classname.startswith(
        "file:"
    ):  # Deal with the class that provided by users
        class_file_and_name = user_provide_classname.split("file:")[-1]
        package_and_class_parts = class_file_and_name.split(".")
        try:
            assert (len(package_and_class_parts)) > 2
        except AssertionError:
            raise AssertionError(
                "The method {!} you provided seems like has a wrong form."
            )
        user_package = ".".join(package_and_class_parts[:-1]).strip()
        user_class = package_and_class_parts[-1].strip()
        return get_class_from_moudle(module=user_package, value=user_class)
    else:
        return get_class_from_spydy(user_provide_classname)


def get_class_from_spydy(class_name):
    try:
        step_class = getattr(spydy, class_name)
    except AttributeError:
        msg = "{!r} not found in spydy".format(class_name)
        raise AttributeError(msg)
    return step_class


def get_class_from_moudle(module=None, value=None):  # packge class
    try:
        user_module = importlib.import_module(name=module)
    except ImportError:
        raise ImportError("Can not import Moudle {!r}".format(module))
    try:
        step_class = getattr(user_module, value)
    except AttributeError:
        raise AttributeError("Class {!r} not in moudle {!r}".format(module, value))
    return step_class


def get_value_from_moulde(*args, **kwargs):
    file_value = get_class_from_moudle(*args, **kwargs)
    if callable(file_value):  # function without args, then call it
        return file_value()
    else:
        return value


def parse_arguments(args: dict) -> dict:
    # breakpoint()
    result_args = {}
    for k, v in args.items():
        if v.startswith("file:"):
            value = get_file_value(v)
        else:
            value = v
        result_args[k] = value
    return result_args


def get_file_value(value):
    user_file_value = value.split("file:")[-1]
    file_and_value_parts = user_file_value.split(".")
    try:
        assert (len(file_and_value_parts)) > 2
    except AssertionError:
        raise AssertionError("The value {!} you provided seems like has a wrong form.")
    user_package = ".".join(file_and_value_parts[:-1]).strip()
    user_value = file_and_value_parts[-1].strip()
    return get_value_from_moulde(module=user_package, value=user_value)


def configs_assertion(configs):
    """
    Confirm if the configs have the right forms
    """
    try:
        assert "PipeLine" in configs
    except AssertionError:
        raise AssertionError("Section <PipeLine> seems not be inclued")
    try:
        assert "Globals" in configs
    except AssertionError:
        raise AssertionError("Section <Globals> seems not be inclued")
    try:
        assert (
            "run_mode" in configs["Globals"]
            and configs["Globals"]["run_mode"] in RUNMODES
        )
    except:
        raise AssertionError(
            "Parameter <run_mode> seems not be provides or run_mode not in {}".format(
                RUNMODES
            )
        )


def linear_pipelinefunc(a, b):
    if callable(a):
        return b(a())
    else:
        return b(a)


def print_pipeline(pipeline: list):
    msg = "Your pipeline looks like :\n" + " ⇨ ".join([str(item) for item in pipeline])
    print(msg + "\n")


def print_msg(msg, info_header="INFO", time_format="%Y-%m-%d %H:%M:%S", verbose=False):
    msg = msg if verbose else repr(msg)
    time_info = datetime.now().strftime(time_format)
    message = "|".join([info_header, time_info, msg])
    print(message)


def get_step_from_pipeline(pipeline, step_type="urls"):
    """
    get a step from pipeline by a given step_type
    """
    if step_type == "url":
        for step in pipeline:
            if isinstance(step, Urls):
                return step
        raise UrlsStepNotFound
    if step_type == "statsLog":
        from spydy.logs import StatsReportLog
        for step in pipeline:
            if isinstance(step, StatsReportLog):
                return step
        return None  # StatsReportLog not found in pipeline     
    else:
        raise StepTypeNotSupported


def get_temp_result(step_type, temp_results, coroutine_id=None):
    """
    Get temp results by step_type and coroutine_id
    """
    if coroutine_id:
        return temp_results[coroutine_id][step_type]
    else:
        return temp_results[step_type]


def get_config_ifexists(parser, section_name, setting_name):
    """
    Get a value of setting in the spydy config file if the setting exists
    """
    try:
        setting_value = parser[section_name][setting_name]
    except KeyError:
        print("{!r} under section {!r} is not found".format(setting_name, section_name))
        return None
    return setting_value


def handle_exceptions(
    run_mode,
    temp_results,
    pipleline: List,
    coroutine_id=None,
    handle_type="url_back_last",
):
    """
    Handle exception during workflow by handle_type

    Args:
      :run_mode: spydy running mode, one of the following modes: once, async_once, forever, async_forever
      :temp_results: temporary results stored by spydy engine after each step
      :coroutine_id: id of a coroutine, got by executes id(asyncio.current_task()), which can distinguish a coroutine from others
      :pipeline: list of spydy pipeline components instance
      :handle_type: choose a way to deal with the exception when encountered an exception
    """
    if run_mode == "once":
        url_step = get_step_from_pipeline(pipleline, step_type="url")
        if hasattr(url_step, "handle_exception"):
            url = get_temp_result(type(url_step), temp_results, coroutine_id)
            url_step.handle_exception(handle_type=handle_type, url=url_for_request(url))


def get_total_from_urls(urls_instance):
    """
    Call 'total' property of a 'Urls' instance to get current remainning number of urls

    Args:
      :urls_instance: instance of a 'Urls' object
    """
    if hasattr(urls_instance, "total"):
        current_total = urls_instance.total
        return current_total
    else:
        return None


def convert_seconds_to_formal(seconds):
    """
    Convert  seconds to a formal time format
    """
    H = int(seconds // 3600)  # Hours
    M = 0  # Minitues
    S = 0  # Seconds

    if H > 0:
        M = int((seconds - 3600 * H) // 60)
        if M > 0:
            S = int(seconds - 3600 * H - 60 * M)
        else:
            S = int(seconds - 3600 * H)
    else:
        M = int(seconds // 60)
        if M > 0:
            S = int(seconds - 60 * M)
        else:
            S = int(seconds)
    return "{}h:{}m:{}s".format(H, M, S)


def print_stats_log(stats: dict):
    """
    Print table-formatted infomations

    Args:
    :stats: A dict object
    """
    output = " {}: {}|" * len(stats)
    output += "\r"
    infos = []
    for h, c in stats.items():
        infos.append(h)
        infos.append(c)
    info_table = output.format(*infos)
    sys.stdout.write(info_table)
    sys.stdout.flush()


