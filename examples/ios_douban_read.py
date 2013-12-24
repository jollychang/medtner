# -*- encoding: utf8 -*-
from selenium import webdriver
driver = webdriver.Remote("http://localhost:3001/wd/hub", webdriver.DesiredCapabilities.FIREFOX)
driver.get('http://read.douban.com')
print driver.title