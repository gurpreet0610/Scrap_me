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
class scrap_page:
    def __init__(self,m_id,year,driver):
        #self.driver = webdriver.Chrome(r'C:\code\driver')
        #self.driver.get(r'https://www.cricbuzz.com/live-cricket-scorecard/10673/csk-vs-dc-5th-match-indian-premier-league-2010')
        self.driver = driver
        #conn = pymongo.MongoClient("mongodb://gurpreet:qwerty123@ds225902.mlab.com:25902/ipl_predictor")
        conn = pymongo.MongoClient("mongodb://gurpreet:qwerty123@ds229312.mlab.com:29312/ipl")
        db = conn.get_database()
        self.col = db['ipl_test']
        #self.insert_db(m_id,year)
        self.insert_csv(m_id,year)
    def insert_csv(self,m_id,year):
        date,city,venue,match_no,team1,team2 = self.match_info()
        self.all_player(m_id,year,match_no,date)
    def insert_db(self,m_id,year):
        check =self.insert_basic(m_id,year)
        self.inning(1,check)
        self.inning(2,check)
    def all_player(self,m_id,year,m_no,date):
        print(m_no)
        for inning in range(1,3):
            for i in range(3,20):
                path='//*[@id="innings_'+str(inning)+'"]/div[1]/div['+str(i)+']'
                x=self.get_text(path)
                tst = re.split('\n',x)
                if  tst[0] == 'Extras':
                    break
                else:
                    l=self.get_list(m_id,year,m_no,x,0,date)
                    self.write_csv(l)
        for inning in range(1,3):
            try:
                ids= self.driver.find_element_by_xpath('//*[@id="innings_'+str(inning)+'"]/div[4]')
                ball = ids.find_elements_by_class_name('cb-scrd-itms')
            except:
                ids= self.driver.find_element_by_xpath('//*[@id="innings_'+str(inning)+'"]/div[2]')
                ball = ids.find_elements_by_class_name('cb-scrd-itms')
            q= len(ball)
            for i in range(2,q+2):
                #//*[@id="innings_2"]/div[2]/div[1]/div[1]
                try:
                    path = '//*[@id="innings_'+str(inning)+'"]/div[4]/div['+str(i)+']'
                    x = self.get_text(path)
                except:
                    path = '//*[@id="innings_'+str(inning)+'"]/div[2]/div['+str(i)+']'
                    x = self.get_text(path)
                l=self.get_list(m_id,year,m_no,x,1,date)
                self.write_csv(l)
    def write_csv(self,l):
        name='2008.csv'
        with open(name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(l)

    def get_list(self,m_id,year,m_no,x,b,date):
        x = self.clear_player(x)
        y = re.split('\n',x)
        if b==0:
            l=[m_id,year,date,m_no,b,y[0],self.get_out(y[1]),int(y[2]),int(y[3]),int(y[4]),int(y[5]),float(y[6]),0,0,0,0,0,0,0]
        else:
            l=[m_id,year,date,m_no,b,y[0],0,0,0,0,0,0,float(y[1]),int(y[2]),int(y[3]),int(y[4]),int(y[5]),int(y[6]),float(y[7])]
        return l

    def get_text(self,xpath):
        x=self.driver.find_element_by_xpath(xpath)
        return x.text

    def clear_player(self,x):
        x = (x.replace(' (c)','')).replace(' (wk)','').replace(' (c & wk)','')
        return x
    def get_squads(self):
        team1_squad = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[10]/div[2]')
        team1_squad= self.clear_player(team1_squad)
        team1_squad=re.split(', ',team1_squad)
        try:
            team2_squad = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[12]/div[2]')
        except:
            team2_squad = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[11]/div[2]')
        team2_squad= self.clear_player(team2_squad)
        team2_squad=re.split(', ',team2_squad)
        return team1_squad, team2_squad
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
    def get_toss(self):
        # get toss details
        toss_get = self.get_text('//*[@id="page-wrapper"]/div[4]/div[2]/div[4]/div[2]/div[3]/div[2]')
        toss_winner,toss_decision=toss_get.split(' won the toss and opt to ')
        return toss_winner,toss_decision
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
    def get_inning(self,innings):
        #//*[@id="innings_1"]/div[1]/div[1]
        bat_1 = self.get_text('//*[@id="innings_'+str(innings)+'"]/div[1]/div[1]')
        team,y = re.split(' Innings\n',bat_1)
        total,i = re.split('-',y)
        return team,total,i[0]
    def get_bat(self,x):
        x = self.clear_player(x)
        y = re.split('\n',x)

        return {"name":y[0],"isout" :self.get_out(y[1]),"run" :int(y[2]),"balls":int(y[3]),"4s":int(y[4]),"6s":int(y[5]),"sr":float(y[6])}

    def get_bats(self,inning,i,a):
        ids= self.driver.find_element_by_xpath('//*[@id="innings_'+str(inning)+'"]/div[1]')
        z=self.col.find_one()
        #//*[@id="innings_1"]/div[1]/div[3]
        #//*[@id="innings_2"]/div[1]/div[3]
        for i in range(3,20):
            path='//*[@id="innings_'+str(inning)+'"]/div[1]/div['+str(i)+']'
            x=self.get_text(path)
            # print(x)
            # print("--------------------------------------------------")
            tst = re.split('\n',x)
            if  tst[0] == 'Extras':
                break
            else:
                sleep(1)
                self.col.update_one({'_id': z['_id']},{ '$push': {"all_info."+str(a)+".batsman":self.get_bat(x)}})
                sleep(1)
    def get_ball(self,x):
        x = self.clear_player(x)
        y = re.split('\n',x)

        return {
            "name":y[0],"over": float(y[1]),"maiden":int(y[2]),"run_conceded":int(y[3]),"wickets_taken":int(y[4]),"no_ball":int(y[5]),"wide_ball":int(y[6]),"economy":float(y[7])
            }

    def get_balls(self,inning,a):
        ids= self.driver.find_element_by_xpath('//*[@id="innings_'+str(inning)+'"]/div[4]')
        ball = ids.find_elements_by_class_name('cb-scrd-itms')
        q= len(ball)
        z=self.col.find_one()
        #//*[@id="innings_1"]/div[4]/div[2]
        #//*[@id="innings_2"]/div[4]/div[2]
        for i in range(2,q+2):
            path = '//*[@id="innings_'+str(inning)+'"]/div[4]/div['+str(i)+']'
            x = self.get_text(path)
            self.col.update_one({'_id': z['_id']},{ '$push': {"all_info."+str(a)+".bowler":self.get_ball(x)}})

    def inning(self,innings,check):
        #ids =self.driver.find_element_by_id('innings_'+innings)
        team,total,i = self.get_inning(innings)
        if check == True and innings == 1:
            self.get_bats(innings,i,0)
            self.get_balls(innings,1)
        elif check == True and innings ==2:
            self.get_bats(innings,i,1)
            self.get_balls(innings,0)
        elif check ==False and innings==1:
            self.get_bats(innings,i,1)
            self.get_balls(innings,0)
        elif check ==False and innings==2:
            self.get_bats(innings,i,0)
            self.get_balls(innings,1)

    def insert_basic(self,m_id,year):
        #team_1_total,team_2_total
        date,city,venue,match_no,team1,team2 = self.match_info()
        winner,win_runs,win_wicket = self.get_outcome()
        team1_squad, team2_squad = self.get_squads()
        toss_winner,toss_decision = self.get_toss()
        x,y,z = self.get_inning(1)
        q,w,e = self.get_inning(2)
        if x== team1:
            team_1_total = y
            team_2_total = w
            check = True
        else:
            team_1_total = w
            team_2_total = y
            check = False
        element =self.insert_string(m_id,year,date,city,venue,match_no,win_runs,win_wicket,winner,team1,team2,team1_squad,team2_squad,toss_decision,toss_winner,int(team_1_total),int(team_2_total))
        self.col.insert_one(element)
        return check

    def get_out(self,x):
        if x == 'not out':
            return False
        else:
            return True

    def insert_string(self,m_id,year,date,city,venue,match_no,win_runs,win_wicket,winner,team1,team2,team1_squad,team2_squad,toss_decision,toss_winner,team_1_total,team_2_total):
        SEED_DATA ={   "match_id" :m_id,
            "match_info" : {
                "year" : year,
                "date": date,
                "city": city,
                "venue" : venue,
                "match_no" : match_no,
                "outcome": {
                    "by": {
                    "runs": win_runs,
                    "wickets": win_wicket
                    },
                    "winner":winner
                },
                "teams": [
                    team1,
                    team2
                        ],
                "toss": {
                    "decision": toss_decision,
                    "winner": toss_winner
                    },
                "team_squad":{
                    "team1": team1_squad,
                    "team2": team2_squad
                }

            },
            "all_info":[{
                "team_1" : team1,
                "total" : team_1_total,
                "batsman" : [],
                "bowler" : []
            },
            {
                "team_2" : team2,
                "total" : team_2_total,
                "batsman" : [],
                "bowler" : []

            }
            ]
        }
        return  SEED_DATA

driver = webdriver.Chrome(r'C:\code\driver')

"""
driver.get(r'https://www.cricbuzz.com/live-cricket-scorecard/10557/rcb-vs-kkr-1st-match-indian-premier-league-2008')
c= scrap_page(1,2008,driver)

driver.close()
#'https://www.cricbuzz.com/live-cricket-scorecard/10596/kkr-vs-rr-10th-match-indian-premier-league-2009'"""

#//*[@id="series-matches"]/div[3]/div[3]/div[1]/a[1]

#//*[@id="series-matches"]/div[61]/div[3]/div[1]/a[1]
year = 2008
match_id = 1
for i in range(3,62):
    try:
        driver.get(r"https://www.cricbuzz.com/cricket-series/2058/indian-premier-league-2008/matches")
        path = '//*[@id="series-matches"]/div['+str(i)+']/div[3]/div[1]/a[1]'
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
            scrap_page(match_id,year,driver)
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