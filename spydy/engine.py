import asyncio
from functools import reduce
from configparser import ConfigParser
from requests_html import HTML
from .defaults import *
from .utils import (
    configs_assertion,
    class_dispatcher,
    linear_pipelinefunc,
    print_pipeline,
    parse_arguments,
)


class Engine:
    def __init__(self, configs: ConfigParser):
        self._configs = configs
        self._pipeline = []
        self.setup()
        print_pipeline(self._pipeline)

    def run(self, run_mode):  # 在这里我也需要套一层err-handling
        if run_mode == "once":
            self.run_once()
        if run_mode == "forever":
            self.run_forever()
        if run_mode == "async_once":
            self.run_async_once()
        if run_mode == "async_forever":
            nworkers = int(self._configs["Globals"].get("nworkers", NWORKERS))
            loop = asyncio.get_event_loop()
            self.run_async_forever(loop, nworkers)        

    def run_once(self):
        return reduce(linear_pipelinefunc, self._pipeline)

    def run_once2(self):
        nsteps = len(self._pipeline)
        final_result = None
        if nsteps == 1:
            step = self._pipeline[0]
            try:  # 出现问题如何处理？
                final_result = step() 
            except:
                pass   # 比如在parser这一步出错， 同步任务很简单，只要把中间结果放到self中即可{type(stepclass):result}，异步任务的话{id of ayncio.current_task():}，  并且直接return None
            return final_result
        if nsteps > 1:
            first_step = self._pipeline[0]
            temp_result = first_step()
            for nth in range(1, nsteps):
                cur_step = self._pipeline[nth]
                temp_result = cur_step(temp_result)
            return temp_result
        

    def run_forever(self):
        while True:
            self.run_once()

    async def async_run_once(self):
        nsteps = len(self._pipeline)
        # print("async task name:", asyncio.current_task())
        if nsteps == 1:
            step = self._pipeline[0]
            if step.Async:
                return await step()
            else:
                return step()
        if nsteps > 1:
            first_step = self._pipeline[0]
            if hasattr(first_step, "Async"):
                temp_result = await self._pipeline[0]()  # 改成first_step()
            else:
                temp_result = self._pipeline[0]()
            for nth in range(1, nsteps):
                cur_step = self._pipeline[nth]
                if hasattr(cur_step, "Async"):
                    temp_result = await cur_step(temp_result)
                else:
                    temp_result = cur_step(temp_result)
            return temp_result

    async def async_run_forever(self):
        while True:
            await self.async_run_once()

    def run_async_once(self):
        asyncio.run(self.async_run_once())

    def run_async_forever(self, eventloop, nworkers):
        tasks = [
            asyncio.ensure_future(self.async_run_forever()) for _ in range(nworkers)
        ]
        eventloop.run_until_complete(asyncio.wait(tasks))

    def setup(self):
        for k, v in self._configs["PipeLine"].items():
            step_class = class_dispatcher(v)
            if v in self._configs:
                arguments = parse_arguments(
                    self._configs[v]
                )  # arguments 对应的是一个键值对， 可能是 file
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
