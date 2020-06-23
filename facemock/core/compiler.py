import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from parser import parser_yaml
# is_displayed




# try:
#     # wait for the visibility of the element with text as "No results found"
#     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='No results found']")))
#     # if the element with text as No results found, induce WebDriverWait for invisibilityOfElement obscuring the clickable element
#     new WebDriverWait(driver, 20).until(ExpectedConditions.invisibilityOfElementLocated(By.cssSelector("//div[@class='ut-click-shield showing interaction']")));
#     # once the invisibilityOfElement obscuring the clickable element is achieved, click on the desired element inducing WebDriverWait
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ut-navigation-button-control']"))).click()
# except TimeoutException:
#     # if search for the element with text as "No results found" raises "TimeoutException" exception click on the element with text as "Buy Now" inducing WebDriverWait
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(,. 'Buy Now')]"))).click()

def execute(driver=None, conf={}, location=None, cmd=None, args=[], kwargs={}):
    # if "window_size" in conf:
    #     driver.set_window_size(conf.get("window_size"))
    start = time.time()
    # Open a page
    url = kwargs.get("url")
    driver.get(url)

    location = kwargs.get("location") or location
    cmd = kwargs.get("cmd") or cmd
    byId = kwargs.get("byId")
    byXpath = kwargs.get("byXpath")
    if byId:
        ele = driver.find_element_by_id(byId)
    elif byXpath:
        ele = driver.find_element_by_xpath(byXpath)
    else:
        print("Please don't forget to use a ID or Location")

    if cmd == 'hit':
        pass

    elif cmd == 'click':
        path = kwargs.get("filename")
        value = kwargs.get("value")
        # element = driver.find_element_by_xpath(location)
        # location a position --> text
        # driver.find_element_by_id('kw').send_keys(value)
        # location a button --> click
        # driver.find_element_by_id('su').click()
        ele.send_keys(value)
        driver.find_element_by_id('su').click()
        time.sleep(3)
        # ret = element.click()
        driver.get_screenshot_as_file(path)
        print("click done -->", 'done')
        # need to wait here
        # time.sleep(3)
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
    print(" Cost time: {} seconds".format(time.time() - start))

def main():
    driver = webdriver.Remote('http://localhost:5555/wd/hub', DesiredCapabilities.FIREFOX)
    # target = 'http://www.baidu.com/'
    driver.set_window_size(1280, 1024)
    # execute(driver=driver, location=target, cmd='save_screenshot', kwargs={'filename': 'screenshot.png'})

    # load yaml
    case = parser_yaml('./examples/test.yaml')
    group = case.get("A")
    steps = group.get("steps")
    for step in steps:
        print("step -->", step)
        execute(driver, kwargs=step)

if __name__ == '__main__':
    main()
