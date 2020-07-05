import time
import os
from datetime import datetime

now = datetime.now() # current date and time
META_PATH = "./assets/{}/".format(now.strftime("%Y%m%d%H%M"))
try:
    if os.path.isfile(META_PATH):
        print("File has been created")
    else:
        os.mkdir(META_PATH)
except Exception as e:
    print("Failure to create assets dir", e)

try:
    os.mkdir(META_PATH + "icon/")
except Exception as e:
    print("Failure to create assets dir", e)

class Action(object):
    def __init__(self, driver, dest):
        self.driver = driver
        self.dest =  dest
        self.ele = None
        # self.meta = meta
        # url = kwargs.get("url") or self.driver.current_url

    def setValue(self, **kwargs):
        self.ele.send_keys(value)
        path = kwargs.get("filename") or '{}setValue_at_{}_.png'.format(META_PATH, int(time.time()))
        ret = {"path": path}
        return ret

    def click(self, **kwargs):
        print("click ...")
        # timeout = kwargs.get("delay")
        # timeout = int(timeout)
        timeout = 5
        self.ele.click()
        time.sleep(timeout)
        path = kwargs.get("filename") or '{}click_at_{}_.png'.format(META_PATH, int(time.time()))
        ret = {"path": path}
        return ret

    def switchTo(self, **kwargs):
        path = kwargs.get("filename") or '{}switchTo_at_{}_.png'.format(META_PATH, int(time.time()))
        windows = self.driver.window_handles
        print("windows: {}".format(len(windows)))
        for window in windows:
            pass
        self.driver.switch_to.window(window)
        need_mark = False
        ret = {"path": path}
        return ret

    def screenshot(self, **kwargs):
        path = kwargs.get("filename") or '{}shot_at_{}_.png'.format(META_PATH, int(time.time()))
        self.driver.get_screenshot_as_file(path)
        ret = {"path": path}
        return ret


def main():
    action = Action('driver')

    kwargs = {
        "name": "frank",
        "age": 28
    }
    exec_action(action= action, cmd = 'click', kwargs=kwargs)


if __name__ == '__main__':
    main()
