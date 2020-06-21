from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote('http://localhost:5555/wd/hub', DesiredCapabilities.FIREFOX)

#browser = webdriver.Firefox()
#browser.get('http://seleniumhq.org/')
target = 'http://seleniumhq.org/'
driver.set_window_size(1280, 1024)
driver.get(target)
driver.save_screenshot('info.png')
