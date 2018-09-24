from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import dateparser
import re
import csv

team= 'Sunrisers Hyderabad'
x ='Bhuvneshwar Kumar, Shikhar Dhawan, Shakib Al Hasan, Kane Williamson(c), Manish Pandey, Carlos Brathwaite, Yusuf Pathan, Wriddhiman Saha, Rashid Khan, Ricky Bhui, Deepak Hooda, Siddarth Kaul, T Natarajan, Mohammad Nabi, Basil Thampi, K Khaleel Ahmed, Sandeep Sharma, Sachin Baby, Chris Jordan, Tanmay Agarwal, Shreevats Goswami, Bipul Sharma, Mehdi Hasan, Alex Hales'

x = (((x.replace(' (c)','')).replace(' (wk)','').replace(' (c & wk)','').replace('(c)','')).replace('(wk)','')).replace('(c & wk)','')
squad=re.split(', ',x)
l = [team] +squad
name='squad.csv'
with open(name, 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(l)
for i in squad:
    j = [i] + [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    with open('player.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(j)
