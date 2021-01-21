from functools import reduce
import importlib
import spydy
from .defaults import RUNMODES


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
