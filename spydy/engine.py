import asyncio
import time
from functools import reduce
from collections import defaultdict
from typing import Union
from configparser import ConfigParser
from requests.exceptions import RequestException
from requests_html import HTML
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
    handle_exceptions,
    get_step_from_pipeline,
)


class Engine:
    def __init__(self, configs: Union[ConfigParser, dict]):
        self._configs = configs
        self._pipeline = []
        self._temp_results = {}
        self._interval = (
            int(self._configs["Globals"].get("interval", None))
            if self._configs["Globals"].get("interval", None)
            else None
        )
        self._exceptions_records = defaultdict(int)
        self.setup()
        print_pipeline(self._pipeline)

    def run(self):  # TODO : exception hanler for success exception is not that good,
        run_mode = self._configs["Globals"].get("run_mode")
        if run_mode == "once":
            try:
                self.run_once()
            except Exceptions_Of_Success as e:
                print_msg(
                    msg="Task Done, Details:" + str(e),
                    info_header="SUCCESS",
                    verbose=True,
                )
        if run_mode == "forever":
            try:
                self.run_forever()
            except Exceptions_Of_Success as e:
                print_msg(
                    msg="Task Done, Details:" + str(e),
                    info_header="SUCCESS",
                    verbose=True,
                )

        if run_mode == "async_once":
            try:
                self.run_async_once()
            except Exceptions_Of_Success as e:
                print_msg(
                    msg="Task Done, Details:" + str(e),
                    info_header="SUCCESS",
                    verbose=True,
                )

        if run_mode == "async_forever":
            nworkers = int(self._configs["Globals"].get("nworkers", NWORKERS))
            loop = asyncio.get_event_loop()
            tasks = self.run_async_forever(loop, nworkers)
            for task in tasks:
                exception = task.exception()
                for success_exception in Exceptions_Of_Success:
                    if isinstance(exception, success_exception):
                        print_msg(
                            msg="Task Done, Details:" + str(exception),
                            info_header="SUCCESS",
                            verbose=True,
                        )
                    else:
                        raise

        self.close()

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
                    self._exceptions_records[type(e)] += 0
                    handle_exceptions(
                        temp_results=self._temp_results,
                        pipleline=self._pipeline,
                        recovery_type=self._configs["Globals"].get(
                            "recovery_type", RECOVERY_TYPE
                        ),
                    )
                    temp_result = None
                except Exceptions_To_Ignore as e:
                    self._exceptions_records[type(e)] += 0
                    handle_exceptions(
                        temp_results=self._temp_results,
                        pipleline=self._pipeline,
                        recovery_type="skip",
                    )
                    temp_result = None
                except Exceptions_To_RunAgain as e:
                    self._exceptions_records[type(e)] += 0
                    handle_exceptions(
                        temp_results=self._temp_results,
                        pipleline=self._pipeline,
                        recovery_type="url_back_end",
                    )
                    temp_result = None
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
                    self._exceptions_records[type(e)] += 1
                    handle_exceptions(
                        temp_results=self._temp_results,
                        pipleline=self._pipeline,
                        coroutine_id=_coroutine_id,
                        recovery_type=self._configs["Globals"].get(
                            "recovery_type", RECOVERY_TYPE
                        ),
                    )
                    temp_result = None
                except Exceptions_To_Ignore as e:
                    self._exceptions_records[type(e)] += 0
                    handle_exceptions(
                        temp_results=self._temp_results,
                        pipleline=self._pipeline,
                        recovery_type="skip",
                    )
                    temp_result = None
                except Exceptions_To_RunAgain as e:
                    self._exceptions_records[type(e)] += 0
                    handle_exceptions(
                        temp_results=self._temp_results,
                        pipleline=self._pipeline,
                        recovery_type="url_back_end",
                    )
                    temp_result = None
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
        for k, v in self._configs["PipeLine"].items():
            step_class = class_dispatcher(v)
            if k in self._configs:
                arguments = parse_arguments(self._configs[k])
                try:
                    self._pipeline.append(step_class(**arguments))
                except TypeError as e:
                    err_msg = (
                        "Class {!r} encounter an error when instantiating: {}".format(
                            step_class, e.args
                        )
                    )
                    raise TypeError(err_msg)
            else:
                self._pipeline.append(step_class())

        # Prepare statsReportLog if exists
        statsReportLog_instance = get_step_from_pipeline(
            self._pipeline, step_type="statsLog"
        )
        if statsReportLog_instance:
            ulrs_instance = get_step_from_pipeline(self._pipeline, step_type="url")
            statsReportLog_instance._urls_instance = ulrs_instance
            statsReportLog_instance.init()

    def close(self):
        if self._exceptions_records:
            print("😭 Finished! But encounterd several ecceptions during running:")
            for k, v in sorted(
                self._exceptions_records.items(), key=lambda item: item[1], reverse=True
            ):
                print(k, " : ", v)
        else:
            print("😊 Completed! Spydy ran successfully without any excepitons")
