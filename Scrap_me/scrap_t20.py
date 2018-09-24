from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.chrome.options import Options
import dateparser
import re
import pymongo
import csv


def search(name,driver):
    driver.get(r"http://www.espncricinfo.com/ci/content/player/index.html")
    x = (driver.find_element_by_xpath('//*[@id="ProfilesearchTxtBox"]'))
    x.clear()
    x.send_keys(name)
    x.send_keys(u'\ue007')
    y = driver.find_element_by_xpath('//*[@id="ciHomeContentlhs"]/div[5]/div/p[2]/a')
    y.click()
    y = driver.find_element_by_xpath('//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[6]/td[1]/a')
    y.click()

options=Options()
options.add_argument('--log-level=3')
name = 'MS Dhoni'
driver = webdriver.Chrome(r'C:\code\driver',options=options)

search(name,driver)