from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
import dateparser
import re
import pymongo
import csv
def create_csv(path, name,driver):
        table_obj = driver.find_element_by_xpath(path)
        rows = table_obj.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")
            if len(col) != 0:
                input_csv = [col[0].text, col[1].text, col[2].text, col[3].text,col[4].text, col[5].text]
                with open(name, 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(input_csv)
        sleep(3)
#name = 'virat kholi'
driver = webdriver.Chrome(r'C:\code\driver')
driver.get(r'https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/all-time')
"""
x = (driver.find_element_by_xpath('//*[@id="lst-ib"]'))
x.send_keys(name +' ipl')
x.send_keys(u'\ue007')
y = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/h3/a')
y.click()

t1_path ='//*[@id="main-content"]/div[1]/div/table[1]/tbody'
t2='//*[@id="main-content"]/div[1]/div/table[2]/tbody'
"""
name='boc.csv'
path='//*[@id="page_filling_chart"]/center/table/tbody'
create_csv(path,name,driver)
