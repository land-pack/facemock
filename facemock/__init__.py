import os
import time
import concurrent.futures
import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .core import parser
from .core import compiler as cc
from .core import parser


class Facemock(object):

    def __init__(self, *args, **kwargs):
        # TODO： If you use multi-thread, don't declare driver here .
        self.driver = webdriver.Remote('http://localhost:5555/wd/hub', DesiredCapabilities.FIREFOX)
        self.driver.set_window_size(1280, 1024)


    def load_case(self, input="./case", max_workers=None):
        """
        An Executor subclass that executes calls asynchronously
        using a pool of at most max_workers processes. If max_workers
        is None or not given, it will default to the number of processors
        on the machine.
        """
        print("Loading case ...")
        cases =[ "{}/{}".format(input, i) for i in os.listdir(input) if i.endswith(".yaml")]
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for  i  in zip(cases, executor.map(parser.do_parser, cases)):
                print('Parser return: {}'.format(i))

    def _load_case(self, filename):
        case = parser.parser_yaml(filename)
        for group_name in case.keys():
            group = case.get(group_name)
            print("case -->", group)
            target = group.get("target")
            steps = group.get("steps")

            conf = {
                "target": target
            }
            for step in steps:
                print("step -->", step)
                cc.route_execute(self.driver, conf=conf, kwargs=step)

    def _execute(self, filename):
        # t_id = threading.current_thread()
        p_id = os.getpid()
        start_t = time.time()
        # do really stuff here.
        # time.sleep(1)
        self._load_case(filename)
        # finish task
        cost = time.time() - start_t
        print("Pid:{} \nCost:{} sec\nFilename:{}".format(p_id, cost, filename))

    def exec_case(self, input="./meta", max_workers=4):
        print("Executing case ...")
        cases =[ "{}/{}".format(input, i) for i in os.listdir(input) if i.endswith(".yaml")]
        # cases = ["file/{}".format(i) for i in range(30)]
        total_cases =  len(cases)
        print("-" * 45)
        print("Total cases: {} ".format(total_cases))
        print("Max workers: {} ".format(max_workers))
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for  i  in zip(cases, executor.map(self._execute, cases)):
                print('Parser return: {}'.format(i))

    def run(self):
        print("Start ....")
