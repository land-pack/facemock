import yaml
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from parser import parser_yaml


def execute(driver=None, conf={}, location=None, cmd=None, args=[], kwargs={}):
    # if "window_size" in conf:
    #     driver.set_window_size(conf.get("window_size"))
    location = kwargs.get("location") or location
    cmd = kwargs.get("cmd") or cmd


    if cmd == 'click':
        element = driver.find_element_by_xpath(location)
        element.click()
        print("click done -->", element)
    elif cmd == 'screenshot':
        path = kwargs.get("filename") or cmd
        print("take a shot ", path)
        driver.get_screenshot_as_file(path)
    else:

        try:
            driver.get(location)
            func = getattr(driver, cmd)
            p = kwargs.get("filename")
            func(p)

        except AttributeError:
            print("dostuff not found")

def main():
    driver = webdriver.Remote('http://localhost:5555/wd/hub', DesiredCapabilities.FIREFOX)
    # target = 'http://www.baidu.com/'
    driver.set_window_size(1280, 1024)
    # execute(driver=driver, location=target, cmd='save_screenshot', kwargs={'filename': 'screenshot.png'})

    # load yaml
    case = parser_yaml('./examples/test.yaml')
    group = case.get("A")
    steps = group.get("steps")
    # print('steps -->', steps)
    for step in steps:
        # step = steps[0]
        print("step -->", step)
        execute(driver, kwargs=step)

if __name__ == '__main__':
    main()
