import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from parser import parser_yaml
from mark import mark_mouse

META_PATH = "./meta/"

def execute(driver=None, conf={},  kwargs={}):
    target = conf.get("target")
    # if "window_size" in conf:
    #     driver.set_window_size(conf.get("window_size"))
    start = time.time()
    # Open a page
    url = kwargs.get("url") or driver.current_url
    is_first_time_in = False
    if "about:blank" in url:
        first_time_in = True
        url = target
        driver.get(url)

    print("Target url:", url)
    # driver.get(url)
    location = kwargs.get("location")
    cmd = kwargs.get("cmd") or cmd
    byId = kwargs.get("byId")
    byXpath = kwargs.get("byXpath")
    delay = kwargs.get("delay")

    if byId:
        mark_key = byId
        ele = driver.find_element_by_id(byId)
    elif byXpath:
        mark_key = byXpath
        ele = driver.find_element_by_xpath(byXpath)
    else:
        print("Please don't forget to use a ID or Location")

    value = kwargs.get("value")
    need_mark = True

    if cmd == 'setValue':
        ele.send_keys(value)
        path = kwargs.get("filename") or '{}setValue_at_{}_.png'.format(META_PATH, int(time.time()))

    elif cmd == 'click':
        ele.click()
        path = kwargs.get("filename") or '{}click_at_{}_.png'.format(META_PATH, int(time.time()))
        time.sleep(int(delay))

    elif cmd == 'switchTo':
        path = kwargs.get("filename") or '{}switchTo_at_{}_.png'.format(META_PATH, int(time.time()))
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
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

    driver.get_screenshot_as_file(path)
    if need_mark:
        mark_mouse(path, ele.rect)
    print("Done: cmd={} | path={} |  seconds={}".format(cmd, path, time.time() - start))

def test():
    driver = webdriver.Remote('http://localhost:5555/wd/hub', DesiredCapabilities.FIREFOX)
    driver.set_window_size(1280, 1024)

    # load yaml
    case = parser_yaml('./examples/klook.yaml')
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
    test()
