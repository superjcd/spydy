import asyncio
import time
from functools import reduce
from collections import defaultdict
from typing import Union, List
from configparser import ConfigParser
from requests.exceptions import RequestException
from requests_html import HTML
from .component import Component
from .defaults import *
from .exceptions import (
    Exceptions_To_Handle,
    Exceptions_To_Ignore,
    Exceptions_Of_Success,
    Exceptions_To_RunAgain,
)
from .utils import (
    class_dispatcher,
    print_pipeline,
    print_msg,
    parse_arguments,
    get_interval,
    get_verbose,
    get_recovery_type,
    handle_exceptions,
    get_step_from_pipeline,
    wrap_exceptions_message,
    print_table,
)


_SPYDY_CONFIGS = Union[ConfigParser, dict]


def _init_pipeline(configs: _SPYDY_CONFIGS, pipeline: list):
    """
    Initialize the pipeline based on the configs
    """
    if isinstance(configs, ConfigParser):
        for k, v in configs["PipeLine"].items():
            step_class = class_dispatcher(v)
            if k in configs:
                arguments = parse_arguments(configs[k])
                try:
                    pipeline.append(step_class(**arguments))
                except TypeError as e:
                    err_msg = (
                        "Class {!r} encounter an error when instantiating: {}".format(
                            step_class, e.args
                        )
                    )
                    raise TypeError(err_msg)
            else:
                pipeline.append(step_class())
    if isinstance(configs, dict):
        pipeline.extend(configs["PipeLine"])


def _init_statsReport(pipeline):
    """
    Initialize the StatsReportLog instance in pipeline if exists
    """
    statsReportLog_instance = get_step_from_pipeline(pipeline, step_type="statsLog")
    if statsReportLog_instance:
        ulrs_instance = get_step_from_pipeline(pipeline, step_type="url")
        statsReportLog_instance.init(ulrs_instance)


def _init_exceptionLog(pipeline, excepitons):
    """
    Initialize the ExceptionLog instance in pipeline if exists
    """
    exceptionLog_instance = get_step_from_pipeline(pipeline, step_type="exceptionLog")
    if exceptionLog_instance:
        exceptionLog_instance.init(excepitons)


def handle_erroneous_exceptions(
    exception, verbose_flag, excepitons_records, temp_results, pipeline, recovery_type
):
    """
    Handle exceptions while running through the pipeline
    """
    if verbose_flag == True:
        if exception:
            print(
                "{} was encountered, details: {}".format(
                    type(exception), exception.args
                )
            )

    if exception:
        excepitons_records[wrap_exceptions_message(exception)] += 1

    handle_exceptions(
        temp_results=temp_results,
        pipeline=pipeline,
        recovery_type=recovery_type,
    )


class Engine:
    def __init__(self, configs: _SPYDY_CONFIGS = None):
        self._configs = configs
        self._pipeline = []
        self._temp_results = {}
        self._interval = get_interval(self._configs)
        self._verbose = get_verbose(self._configs)
        self._exceptions_records = defaultdict(int)
        self.setup()
        print_pipeline(self._pipeline)

    @classmethod
    def from_configparser(cls, configs: ConfigParser):
        return cls(configs)

    @classmethod
    def from_dict(cls, configs: dict):
        return cls(configs)

    def run(self):
        run_mode = self._configs["Globals"].get("run_mode")
        if run_mode in ["once", "forever", "async_once"]:
            self._run(run_mode)

        if run_mode == "async_forever":
            self._run_async_forever()

        self._close()

    def _run(self, run_mode):
        try:
            if run_mode == "once":
                self.run_once()

            if run_mode == "forever":
                self.run_forever()

            if run_mode == "async_once":
                self.run_async_once()
        except Exceptions_Of_Success as e:
            if self._verbose:
                print_msg(
                    msg="Task Done, Details:" + str(e),
                    info_header="SUCCESS",
                    verbose=True,
                )

    def _run_async_forever(self):
        nworkers = int(self._configs["Globals"].get("nworkers", NWORKERS))
        loop = asyncio.get_event_loop()
        tasks = self.run_async_forever(loop, nworkers)
        for task in tasks:
            exception = task.exception()
            for success_exception in Exceptions_Of_Success:
                if isinstance(exception, success_exception):
                    if self._verbose:
                        print_msg(
                            msg="Task Done, Details:" + str(exception),
                            info_header="SUCCESS",
                            verbose=True,
                        )
                else:
                    raise

    def run_once(self):
        final_result = None
        nsteps = len(self._pipeline)
        assert nsteps >= 1
        first_step = self._pipeline[0]
        if nsteps == 1:
            return first_step()
        if nsteps > 1:
            first_step = self._pipeline[0]
            temp_result = first_step()
            self._temp_results[type(first_step)] = temp_result
            for nth in range(1, nsteps):
                cur_step = self._pipeline[nth]
                try:
                    temp_result = cur_step(temp_result)
                except Exceptions_To_Handle as e:
                    handle_erroneous_exceptions(
                        exception=e,
                        verbose_flag=self._verbose,
                        excepitons_records=self._exceptions_records,
                        temp_results=self._temp_results,
                        pipeline=self._pipeline,
                        recovery_type=get_recovery_type(self._configs),
                    )
                    temp_result = None
                except Exceptions_To_Ignore as e:
                    handle_erroneous_exceptions(
                        exception=e,
                        verbose_flag=self._verbose,
                        excepitons_records=self._exceptions_records,
                        temp_results=self._temp_results,
                        pipeline=self._pipeline,
                        recovery_type="skip",
                    )
                    temp_result = None
                except Exceptions_To_RunAgain as e:
                    handle_erroneous_exceptions(
                        exception=e,
                        verbose_flag=self._verbose,
                        excepitons_records=self._exceptions_records,
                        temp_results=self._temp_results,
                        pipeline=self._pipeline,
                        recovery_type="url_back_end",
                    )
                    temp_result = None
                except:
                    handle_erroneous_exceptions(
                        exception=None,
                        verbose_flag=self._verbose,
                        excepitons_records=self._exceptions_records,
                        temp_results=self._temp_results,
                        pipeline=self._pipeline,
                        recovery_type="url_back_end",
                    )
                    raise
                self._temp_results[type(cur_step)] = temp_result
            final_result = temp_result
            return final_result

    def run_forever(self):
        while True:
            if self._interval:
                time.sleep(self._interval)
            self.run_once()
        print_msg(msg="Task Done!", info_header="SUCCESS")

    async def async_run_once(self):
        final_result = None
        nsteps = len(self._pipeline)
        assert nsteps >= 1
        first_step = self._pipeline[0]
        _coroutine_id = id(asyncio.current_task())
        if nsteps == 1:
            if step.Async:
                return await first_step()
            else:
                return step()
        if nsteps > 1:
            first_step = self._pipeline[0]
            if hasattr(first_step, "Async"):
                temp_result = await first_step()
            else:
                temp_result = self._pipeline[0]()
            self._temp_results[type(first_step)] = temp_result
            for nth in range(1, nsteps):
                cur_step = self._pipeline[nth]
                try:
                    if hasattr(cur_step, "Async"):
                        temp_result = await cur_step(temp_result)
                    else:
                        temp_result = cur_step(temp_result)
                except Exceptions_To_Handle as e:
                    self._exceptions_records[wrap_exceptions_message(e)] += 1
                    handle_erroneous_exceptions(
                        exception=e,
                        verbose_flag=self._verbose,
                        excepitons_records=self._exceptions_records,
                        temp_results=self._temp_results,
                        pipeline=self._pipeline,
                        recovery_type=get_recovery_type(self._configs),
                    )
                    temp_result = None
                except Exceptions_To_Ignore as e:
                    handle_erroneous_exceptions(
                        exception=e,
                        verbose_flag=self._verbose,
                        excepitons_records=self._exceptions_records,
                        temp_results=self._temp_results,
                        pipeline=self._pipeline,
                        recovery_type="skip",
                    )
                    temp_result = None
                except Exceptions_To_RunAgain as e:
                    handle_erroneous_exceptions(
                        exception=e,
                        verbose_flag=self._verbose,
                        excepitons_records=self._exceptions_records,
                        temp_results=self._temp_results,
                        pipeline=self._pipeline,
                        recovery_type="url_back_end",
                    )
                    temp_result = None
                except:
                    handle_erroneous_exceptions(
                        exception=None,
                        verbose_flag=self._verbose,
                        excepitons_records=self._exceptions_records,
                        temp_results=self._temp_results,
                        pipeline=self._pipeline,
                        recovery_type="url_back_end",
                    )
                    raise
                self._temp_results[type(cur_step)] = temp_result
            final_result = temp_result
            return temp_result

    async def async_run_forever(self):
        while True:
            if self._interval:
                await asyncio.sleep(self._interval)
            await self.async_run_once()

    def run_async_once(self):
        asyncio.run(self.async_run_once())

    def run_async_forever(self, eventloop, nworkers):
        tasks = [
            asyncio.ensure_future(self.async_run_forever()) for _ in range(nworkers)
        ]
        eventloop.run_until_complete(asyncio.wait(tasks))
        return tasks

    def setup(self):
        _init_pipeline(self._configs, self._pipeline)
        _init_statsReport(pipeline=self._pipeline)
        _init_exceptionLog(pipeline=self._pipeline, excepitons=self._exceptions_records)

    def _close(self):
        if self._exceptions_records:
            print("😭 Finished! But encounterd several ecceptions during running:")
            print_table(self._exceptions_records)
        else:
            print("😊 Completed! Spydy ran successfully without any excepitons")
