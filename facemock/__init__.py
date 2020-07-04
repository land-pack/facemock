import os
import time
import concurrent.futures
import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import (
                             InvalidArgumentException,
                             NoSuchElementException,
                             WebDriverException,
                             TimeoutException)
from .core import parser
from .core import compiler as cc
from .core import parser
from .action import Action
from .core.mark import collect_info


class Facemock(object):

    def __init__(self, *args, **kwargs):
        self.handler_driver_time = 0
        self.last_url = None
        t = time.time()
        self.time_out = 30


        try:
            print("Start to connect webdriver")
            self.driver = webdriver.Remote('http://localhost:5555/wd/hub', DesiredCapabilities.FIREFOX)
            self.handler_driver_time = time.time() - t
            _ = self.driver.implicitly_wait(self.time_out)

        except TimeoutException:
            raise TimeoutException("TimeoutException")
        else:
            print("Get driver successful! {}".format(self.handler_driver_time))

        self.driver.set_window_size(1280, 1024)
        dest = "https://www.klook.com"
        self.action = Action(self.driver, dest)

    def load_case(self, input="./case", max_workers=None):
        """
        An Executor subclass that executes calls asynchronously
        using a pool of at most max_workers processes. If max_workers
        is None or not given, it will default to the number of processors
        on the machine.
        """
        cases =[ "{}/{}".format(input, i) for i in os.listdir(input) if i.endswith(".yaml")]
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for  i  in zip(cases, executor.map(parser.do_parser, cases)):
                print('--> Parser return: {}'.format(i))

    def _find_ele(self, kwargs):
        kwargs = kwargs.get("kwargs")
        print("kw -->", kwargs)
        byId = kwargs.get("byId")
        byXpath = kwargs.get("byXpath")
        print("byXpath", byXpath)
        if byId:
            mark_key = byId
            try:
                self.action.ele = self.driver.find_element_by_id(byId)
            except NoSuchElementException:
                print("NoSuchElementException: {} | with {}".format(byId, ))
                return self.action.ele
        elif byXpath:
            mark_key = byXpath
            try:
                self.action.ele = self.driver.find_element_by_xpath(byXpath)
            except NoSuchElementException:
                print("NoSuchElementException: {}".format(byXpath))
                return self.action.ele
        else:
            return "Can't found ele"



    def exec_action(self, **kwargs):

        start_t = time.time()
        target = "https://www.klook.com"
        start = time.time()
        # Open a page
        url = kwargs.get("url") or self.driver.current_url
        is_first_time_in = False
        is_not_the_same_url = self.last_url != url

        print("is_not_the_same_url: ".format(is_not_the_same_url))

        if "about:blank" in url:
            first_time_in = True
            url = target

            try:
                self.driver.get(url)
            except InvalidArgumentException:
                print("Url error:", url)
                return
            else:
                print("=" * 45)
                print("Title: ", self.driver.title)
                print("=" * 45)

        ele = self._find_ele(kwargs)
        print("is ele display:{}".format(ele))

        try:
            kwargs = kwargs.get("kwargs")
            print("kwargs -->", kwargs)
            cmd = kwargs.get("cmd")
            print(kwargs)
            print("cmd ->", cmd)
            func = getattr(self.action, cmd)
            ret = func(kwargs=kwargs)
            # screenshot at the end
            path = ret.get("path")
            print("path for screenshot: {} | {}".format(path, ret))
            self.driver.get_screenshot_as_file(path)
            end_t = 0
            need_mark = True
            if need_mark:
                collect_info(path, self.action.ele.rect, end_t)


        except AttributeError:
            print("dostuff not found")
            return

    def _load_case(self, filename):
        case = parser.parser_yaml(filename)
        # action = Action('driver')
        for group_name in case.keys():
            group = case.get(group_name)
            target = group.get("target")
            steps = group.get("steps")

            conf = {
                "target": target
            }
            for step in steps:
                t = time.time()
                print("start step: {}".format(step))
                # cc.route_execute(self.driver, conf=conf, kwargs=step)
                # kwargs = step.get("kwargs")
                self.exec_action(kwargs=step)
                print("next step cost: {}".format(time.time() - t))

    def _execute(self, filename):

        p_id = os.getpid()
        print("Worker: {} has wake up".format(p_id))
        start_t = time.time()
        # do really stuff here.
        self._load_case(filename)
        # finish task
        cost = time.time() - start_t
        return "Pid:{} Cost:{} sec Filename:{}".format(p_id, cost, filename)

    def exec_case(self, input="./meta", max_workers=4):
        print("Executing case ...")
        cases =[ "{}/{}".format(input, i) for i in os.listdir(input) if i.endswith(".yaml")]
        total_cases =  len(cases)
        print("-" * 45)
        print("Total cases: {} ".format(total_cases))
        print("Max workers: {} ".format(max_workers))
        print("-" * 45)
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for  i  in zip(cases, executor.map(self._execute, cases)):
                print('{}'.format(i))

    def static_server(self):
        pass

    def dash_server(self):
        pass

    def run(self):
        print("Start ....")
