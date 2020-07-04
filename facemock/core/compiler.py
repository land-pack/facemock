import time
import os
from datetime import datetime
import yaml
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import (
                             InvalidArgumentException,
                             NoSuchElementException,
                             WebDriverException)

from .parser import parser_yaml
from .mark import mark_rect

now = datetime.now() # current date and time
META_PATH = "./assets/{}/".format(now.strftime("%Y%m%d%H%M"))
os.mkdir(META_PATH)






def route_execute(driver=None, conf={},  kwargs={}):
    start_t = time.time()
    target = conf.get("target")
    start = time.time()
    # Open a page
    url = kwargs.get("url") or driver.current_url
    is_first_time_in = False
    if "about:blank" in url:
        first_time_in = True
        url = target
        try:
            driver.get(url)
        except InvalidArgumentException:
            print("Url error:", url)
            return


    print("Target url:", url)
    location = kwargs.get("location")
    cmd = kwargs.get("cmd") or cmd
    byId = kwargs.get("byId")
    byXpath = kwargs.get("byXpath")
    delay = kwargs.get("delay")

    if byId:
        mark_key = byId
        try:
            ele = driver.find_element_by_id(byId)
        except NoSuchElementException:
            print("NoSuchElementException: {} | with {}".format(byId, ))
            return
    elif byXpath:
        mark_key = byXpath
        try:
            ele = driver.find_element_by_xpath(byXpath)
        except NoSuchElementException:
            print("NoSuchElementException: {}".format(byXpath))
            return

    else:
        print("A Sp command don't need to use location. like new window")

    value = kwargs.get("value")
    need_mark = True

    if cmd == 'setValue':
        ele.send_keys(value)
        path = kwargs.get("filename") or '{}setValue_at_{}_.png'.format(META_PATH, int(time.time()))

    elif cmd == 'click':
        ele.click()
        path = kwargs.get("filename") or '{}click_at_{}_.png'.format(META_PATH, int(time.time()))
        # time.sleep(int(delay))

    elif cmd == 'switchTo':
        path = kwargs.get("filename") or '{}switchTo_at_{}_.png'.format(META_PATH, int(time.time()))
        windows = driver.window_handles
        print("windows: {}".format(len(windows)))
        for window in windows:
            pass
        driver.switch_to.window(window)
        need_mark = False

    elif cmd == 'screenshot':
        path = kwargs.get("filename") or '{}shot_at_{}_.png'.format(META_PATH, int(time.time()))
        driver.get_screenshot_as_file(path)
    else:

        try:
            driver.get(url)
            func = getattr(driver, cmd)
            p = kwargs.get("filename")
            func(p)

        except AttributeError:
            print("dostuff not found")
            return

    driver.get_screenshot_as_file(path)
    end_t = time.time() - start_t
    # if need_mark:
    #     collect_info(path, ele.rect, end_t)

    print("Done: cmd={} | path={} |  seconds={}".format(cmd, path, time.time() - start))

def execute_case(driver, filename):

    # # TODO： If you use multi-thread, don't declare driver here .
    # driver = webdriver.Remote('http://localhost:5555/wd/hub', DesiredCapabilities.FIREFOX)
    # driver.set_window_size(1280, 1024)

    # prefix = './meta/'
    # path = prefix + filename
    # load yaml
    case = parser_yaml(filename)
    for group_name in case.keys():
        # group = case.get("A")
        group = case.get(group_name)
        print("case -->", group)
        target = group.get("target")
        steps = group.get("steps")

        conf = {
            "target": target
        }
        for step in steps:
            print("step -->", step)
            execute(driver, conf=conf, kwargs=step)

if __name__ == '__main__':
    filename = './examples/klook.yaml'
    execute_case(filename)
