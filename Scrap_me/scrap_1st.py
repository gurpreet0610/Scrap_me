from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import dateparser
import re
import pymongo
import csv

class scrap_data:
    def __init__(self, year,m_id,driver):
        self.driver = driver
        self.insert_csv(m_id,year)

    def insert_csv(self,m_id,year):
        name='match18.csv'
        date,city,venue,match_no,team1,team2 = self.match_info()
        winner,win_runs,win_wicket = self.get_outcome()
        team1_squad, team2_squad = self.get_squads()
        toss_winner,toss_decision = self.get_toss()
        print(match_no)
        l=[m_id,year,date,match_no,team1,team2,city,venue,toss_winner,toss_decision] +team1_squad + team2_squad+[winner,win_runs,win_wicket]
        with open(name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(l)


    def clear_player(self,x):
        x = (x.replace(' (c)','')).replace(' (wk)','').replace(' (c & wk)','')
        return x

    def get_squads(self):
        team1_squad = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[10]/div[2]')
        #//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[7]/div[2]
        #team1_squad = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[7]/div[2]')
        #//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[10]/div[2]
        #//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[11]/div[2]
        team1_squad= self.clear_player(team1_squad)
        team1_squad=re.split(', ',team1_squad)
        try:
            team2_squad = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[12]/div[2]')
        except Exception as e:
            team2_squad = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[13]/div[2]')
        except:
            team2_squad = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[11]/div[2]')
        team2_squad= self.clear_player(team2_squad)
        team2_squad=re.split(', ',team2_squad)
        return team1_squad, team2_squad
    def get_text(self,xpath):
        x=self.driver.find_element_by_xpath(xpath)
        return x.text

    def get_outcome(self):
        outcome= self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[1]')
        try:
            winner , by = re.split(' won by ',outcome)
            score = re.findall(r'\d+',by)
            score = score[0]
            if 'runs' in by:
                win_runs=int(score)
                win_wicket= None
            else:
                win_runs=None
                win_wicket=int(score)
        except:
            winner = False
            win_runs=False
            win_wicket=False
        return winner,win_runs,win_wicket

    def match_info(self):
        # get_date
        date_get = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[2]/div[2]')
        date=str(dateparser.parse(date_get).date())
        # get place
        place_get = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[5]/div[2]')
        venue,city = place_get.split(', ')
        # get match_details
        match_details = self.get_text('//*[@id="page-wrapper"]/div[4]/div[1]/h1')
        q=re.split(' vs |, ',match_details)
        #q[2]=re.findall(r'\d+',q[2])
        q[2] = q[2].replace(' - Live Cricket Score','')
        team1 =q[0]
        team2=q[1]
        match_no=q[2]
        return date,city,venue,match_no,team1,team2

    def get_toss(self):
        # get toss details
        toss_get = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[3]/div[2]')
        toss_winner,toss_decision=toss_get.split(' won the toss and opt to ')
        return toss_winner,toss_decision
"""name='matches.csv'
l=['m_id','year','date','match_no','team1','team2','city','venue','toss_winner','toss_decision','t1_p1','t1_p2','t1_p3','t1_p4','t1_p5','t1_p6','t1_p7','t1_p8','t1_p9','t1_p10','t1_p11','t2_p1','t2_p2','t2_p3','t2_p4','t2_p5','t2_p6','t2_p7','t2_p8','t2_p9','t2_p10','t2_p11','winner','win_runs','win_wicket']
with open(name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(l)
            """
driver = webdriver.Chrome(r'C:\code\driver')
year = 2018
match_id =645
for i in range(3,63):
    try:
        driver.get(r"https://www.cricbuzz.com/cricket-series/2676/indian-premier-league-2018/matches")
        path ='//*[@id="series-matches"]/div['+str(i)+']/div[3]/div[1]/a[1]'
        element = wait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, path)))
        element.click()
        #y= driver.find_element_by_xpath('//*[@id="matchCenter"]/div[1]/nav/a[2]')
        #y.click()
        driver.implicitly_wait(1)
        sleep(2)
        element1 = wait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="matchCenter"]/div[1]/nav/a[2]')));
        element1.click()
        driver.implicitly_wait(2)
        sleep(3)
        try:
            scrap_data(match_id,year,driver)
            print('done'+str(match_id))
        except Exception as e:
            print('====================================')
            print(e)
            print('------------------------------------')
            print(match_id)
        match_id= match_id+1
    except Exception as e:
        print('====================================')
        print(e)
        print("outside _block" + str(i))
        print('------------------------------------')