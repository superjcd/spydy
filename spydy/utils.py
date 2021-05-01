from datetime import datetime
from typing import List
import reprlib
import importlib
import sys
import spydy
from spydy.urls import Urls
from tabulate import tabulate
from spydy.defaults import (
    SPYDY_DEFUALT_SECTION_NAME,
    RUNMODES,
    LEGAL_GLOBALS,
    LEGAL_RECOVERYS,
    RECOVERY_TYPE,
    VERBOSE,
    LOG_TIME_FORMAT,
)
from spydy.exceptions import UrlsNotFound, StatsLogNotFound, ExceptionLogNotFound
from collections.abc import Iterable


def class_dispatcher(user_provide_classname: str):
    if user_provide_classname.startswith(
        "file:"
    ):  # Deal with the class that provided by users
        class_file_and_name = user_provide_classname.split("file:")[-1]
        package_and_class_parts = class_file_and_name.split(".")
        try:
            assert (len(package_and_class_parts)) > 1
        except AssertionError:
            raise AssertionError(
                "The method {!r} you provided seems like has a wrong form."
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
    import os

    sys.path.append(os.getcwd())
    try:
        user_module = importlib.import_module(name=module)
    except ImportError:
        raise ImportError("Can not import Moudle {!r}".format(module))
    try:
        step_class = getattr(user_module, value)
    except AttributeError:
        raise AttributeError("Class {!r} not in moudle {!r}".format(module, value))
    return step_class


def get_value_from_moudle(*args, **kwargs):
    file_value = get_class_from_moudle(*args, **kwargs)
    return file_value


def parse_arguments(args: dict) -> dict:
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
        assert (len(file_and_value_parts)) > 1
    except AssertionError:
        raise AssertionError("The value {!r} you provided seems like has a wrong form.")
    user_package = ".".join(file_and_value_parts[:-1]).strip()
    user_value = file_and_value_parts[-1].strip()
    return get_value_from_moudle(module=user_package, value=user_value)


def check_configs_and_add_defaults(configs):
    check_configs(configs)
    add_defaults(configs)


def check_configs(configs):
    """
    Configs Sanity checks
    """
    try:
        assert "PipeLine" in configs
    except AssertionError:
        raise ValueError("Section <PipeLine> seems not be inclued")
    try:
        assert "Globals" in configs
    except AssertionError:
        raise ValueError("Section <Globals> seems not be inclued")

    check_run_mode(configs)
    global_arguments = configs["Globals"]
    check_globals_has_legal_keys(global_arguments)

    if "recovery_type" in global_arguments:
        check_recovery_type_in_default_recoverys(global_arguments["recovery_type"])

    check_custom_section_in_pipeline(configs)


def check_globals_has_legal_keys(global_arguments):
    for argument in global_arguments:
        if argument not in LEGAL_GLOBALS:
            raise ValueError(
                "{!r} under [Global] section is not right.Spydy only allows the following settings: {}".format(
                    argument, LEGAL_GLOBALS
                )
            )


def check_run_mode(configs):
    try:
        assert (
            "run_mode" in configs["Globals"]
            and configs["Globals"]["run_mode"] in RUNMODES
        )
    except:
        raise ValueError(
            "Parameter <run_mode> seems not be provides or run_mode not in {}".format(
                RUNMODES
            )
        )


def check_recovery_type_in_default_recoverys(recovery_type):
    if recovery_type not in LEGAL_RECOVERYS:
        raise ValueError(
            "{!r} not in allowed spydy, spydy only supports following recovery types: {}".format(
                recovery_type, LEGAL_RECOVERYS
            )
        )


def check_custom_section_in_pipeline(configs):
    section_names = list(configs)
    right_sections = SPYDY_DEFUALT_SECTION_NAME + list(configs["PipeLine"])

    for section in section_names:
        if section not in right_sections:
            raise ValueError(
                "section name {!r} is wrong, please check if it really sit under [PipeLine] section.".format(
                    section
                )
            )


def add_defaults(configs):
    add_verbose_default(configs)


def add_verbose_default(configs):
    if "verbose" not in configs["Globals"]:
        configs["Globals"]["verbose"] = VERBOSE


def get_verbose(configs):
    try:
        return bool(configs["Globals"].get("verbose", VERBOSE))
    except:
        raise ValueError(
            "Verbose setting in the [Globals] section should can not treated as Bool; Check if you give a right value of verbose"
        )


def get_interval(configs):
    return (
        float(configs["Globals"].get("interval"))
        if configs["Globals"].get("interval", None)
        else None
    )


def get_recovery_type(configs):
    return configs["Globals"].get("recovery_type", RECOVERY_TYPE)


def print_pipeline(pipeline: list):
    msg = "Your pipeline looks like :\n" + " ⇨ ".join([str(item) for item in pipeline])
    print(msg + "\n")


def print_msg(msg, info_header="INFO", time_format=LOG_TIME_FORMAT, verbose=False):
    verbose = bool(verbose)
    msg = msg if verbose else reprlib.repr(msg)
    time_info = get_current_time_string(time_format)
    message = "|".join([info_header, time_info, msg])
    print(message)


def get_current_time_string(fmt):
    return datetime.now().strftime(fmt)


def get_step_from_pipeline(pipeline, step_type):
    """
    Get a step from pipeline by a given step_type
    """
    if step_type == "url":
        for step in pipeline:
            if isinstance(step, Urls):
                return step
        raise UrlsNotFound
    if step_type == "request":
        from spydy.request import Request

        for step in pipeline:
            if isinstance(step, Request):
                return step
        return None
    elif step_type == "statsLog":
        from spydy.logs import StatsReportLog

        for step in pipeline:
            if isinstance(step, StatsReportLog):
                return step
        return None
    elif step_type == "exceptionLog":
        from spydy.logs import ExceptionLog

        for step in pipeline:
            if isinstance(step, ExceptionLog):
                return step
        return None

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
    temp_results,
    pipeline: List,
    coroutine_id=None,
    recovery_type="url_back_end",
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
    url_step = get_step_from_pipeline(pipeline, step_type="url")
    if hasattr(url_step, "handle_exception"):
        url = get_temp_result(type(url_step), temp_results, coroutine_id)
        url_step.handle_exception(recovery_type=recovery_type, url=url)


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


def convert_seconds_to_standard_format(seconds):
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


def print_stats_log(stats: dict, add_time_info=True):
    """
    Print table-formatted infomations

    Args:
    :stats: A dict object
    """
    output = " {}: {}|" * len(stats)
    infos = []
    for h, c in stats.items():
        infos.append(h)
        infos.append(c)
    info_table = output.format(*infos)
    if add_time_info:
        info_table = get_current_time_string(LOG_TIME_FORMAT) + "|" + info_table
    print(info_table)


def wrap_exceptions_message(e, max_length=50):
    full_message = repr(e)
    len_of_message = len(full_message)
    max_oneline_length = 40
    num_msg_slices = len_of_message // max_oneline_length + 1
    last_msg_length = len_of_message % max_oneline_length
    msg_slices = []

    for i in range(num_msg_slices):
        if (i + 1) < num_msg_slices:
            msg_slices.append(
                full_message[i * max_oneline_length : (i + 1) * max_oneline_length]
            )
        else:
            msg_slices.append(
                full_message[
                    i * max_oneline_length : (i * max_oneline_length + last_msg_length)
                ]
            )

    return "\n".join(msg_slices)[:max_length]


def print_table(infos: dict, add_time_info=True):
    table_data = sorted(infos.items(), key=lambda item: item[1], reverse=True)
    table_header = ["ErrorType", "Counts"]
    if add_time_info:
        print(get_current_time_string(fmt=LOG_TIME_FORMAT))
    print(tabulate(table_data, headers=table_header, tablefmt="grid"))


def run_if_callable(val):
    if callable(val):
        return val()
    else:
        return val


def prepare_sql_for_dict(items, table_name):
    item_keys = items.keys()
    col_names = ",".join(item_keys)
    placeholders = ",".join([":" + col for col in item_keys])
    sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
    return sql


def prepare_sql_for_list_of_dict(items: Iterable, table_name):
    data = items[0]
    sql = prepare_sql_for_dict(data)
    return sql
