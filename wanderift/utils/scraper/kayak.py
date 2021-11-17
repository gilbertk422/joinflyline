from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import time
from random import randrange

class Kayak:
    driver = ''

    origin = ''
    destination = ''
    start_date = ''
    return_date = ''

    BOT_MESSAGE = 'Please confirm that you are a real KAYAK user.'

    def __init__(self, origin, destination, start_date, return_date):
        chrome_options = webdriver.ChromeOptions()
        agents = ["Firefox/66.0.3","Chrome/73.0.3683.68","Edge/16.16299"]
        chrome_options.add_argument('--user-agent=' + agents[randrange(len(agents))] + '"')    
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
        self.driver.implicitly_wait(20)

        self.origin = origin
        self.destination = destination
        self.start_date = start_date
        self.return_date = return_date

    def query(self):
        url = "https://www.kayak.com/flights/" + self.origin + "-" + self.destination + "/" + self.start_date + "/" + self.return_date + "?sort=price_a&fs=stops=0"
        self.driver.get(url)

        #Check if site thinks that we're a bot
        time.sleep(5) 
        soup=BeautifulSoup(self.driver.page_source, 'lxml')

        if soup.find_all('p')[0].getText() == self.BOT_MESSAGE:
            self.driver.close()
            time.sleep(20)
            return False
        
        time.sleep(20) #wait 20sec for the page to load

        soup=BeautifulSoup(self.driver.page_source, 'lxml')
    
        #get the arrival and departure times
        deptimes = soup.find_all('span', attrs={'class': 'depart-time base-time'})
        arrtimes = soup.find_all('span', attrs={'class': 'arrival-time base-time'})
        meridies = soup.find_all('span', attrs={'class': 'time-meridiem meridiem'})
    
        deptime = []
        for div in deptimes:
            deptime.append(div.getText()[:-1])    
            
        arrtime = []
        for div in arrtimes:
            arrtime.append(div.getText()[:-1])   

        meridiem = []
        for div in meridies:
            meridiem.append(div.getText())  
            
        deptime = np.asarray(deptime)
        deptime = deptime.reshape(int(len(deptime)/2), 2)
        
        arrtime = np.asarray(arrtime)
        arrtime = arrtime.reshape(int(len(arrtime)/2), 2)      
        
        meridiem = np.asarray(meridiem)
        meridiem = meridiem.reshape(int(len(meridiem)/4), 4)
            
        #Get the price
        regex = re.compile('Common-Booking-MultiBookProvider (.*)multi-row Theme-featured-large(.*)')
        price_list = soup.find_all('div', attrs={'class': regex})
        
        price = []
        for div in price_list:
            price.append(int(div.getText().split('\n')[3][1:-1]))

        results = pd.DataFrame({"origin" : self.origin,
                        "destination" : self.destination,
                        "start_date" : self.start_date,
                        "return_date" : self.return_date,
                        "price": price,
                        "currency": "USD",
                        "deptime_o": [m+str(n) for m,n in zip(deptime[:,0],meridiem[:,0])],
                        "arrtime_d": [m+str(n) for m,n in zip(arrtime[:,0],meridiem[:,1])],
                        "deptime_d": [m+str(n) for m,n in zip(deptime[:,1],meridiem[:,2])],
                        "arrtime_o": [m+str(n) for m,n in zip(arrtime[:,1],meridiem[:,3])]
                        })

        self.driver.close() #close the browser

        time.sleep(15) #wait 15sec until the next request
        
        return results
    
    def run(self):
        data = self.query()
        return data

def main():
    kayak = Kayak(
        origin="MXP",
        destination="ZRH",
        start_date="2020-09-06",
        return_date="2020-09-09",
    )
    print(kayak.run())

if __name__ == "__main__":
    main()