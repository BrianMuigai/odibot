from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver_py import binary_path
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import getpass

class Driver():
    def __init__(self) -> None:
        service_object = Service(binary_path)
        self.browser = webdriver.Chrome(service=service_object)
        self.__login()
        
    def timer(self, t) -> None:
         while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            t -= 1

    def __getUserDetails(self) -> list:
        try:
            file = open('data.csv')
            next(file)
            phone, password, _, __ = next(file).split(',')
            file.close()
            return phone, password
        except:
            file.close()
            print('\n!!!!! There was an error reading phone and password !!!!!\n')
            pass
        print('********** Press enter when you are done **********\n\n')
        phone = input('Please enter your mobile number: ')
        password = getpass.getpass()
        return phone, password
        
    def __login(self) -> None:
        self.browser.get("https://odibets.com")
        print("Getting Odibet...")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mobile-web-login'))
        )

        loginButton = self.browser.find_element(By.CSS_SELECTOR, '#mobile-web-login')
        loginButton.click()
        
        mPhone, mPass = self.__getUserDetails()

        mobile = self.browser.find_element(By.CSS_SELECTOR, '#modal > div > div > div > form > div:nth-child(2) > div > input[type=tel]')
        password = self.browser.find_element(By.CSS_SELECTOR, '#modal > div > div > div > form > div:nth-child(3) > div > input[type=password]')

        mobile.send_keys(mPhone)
        password.send_keys(mPass)
        self.timer(1)

        self.browser.find_element(By.CSS_SELECTOR, '#modal > div > div > div > form > div:nth-child(4) > button').click()
        self.timer(5)

        try:
            self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-header.rich.l-mobile > div.l-header-top > div > a.mybal')
        except:
            print('\n\nSOMETHING WENT WRONG! Please check your credentials and try again\n\n')
            self.__login()

        self.__readBets()

    def __readBets(self):
        file = open('data.csv')
        next(file)
        csvreader = csv.reader(file)

        for row in csvreader:
            _, __, bookingCode, stake = row
            self.__placeBet(bookingCode, stake)

        file.close()

    def __placeBet(self, code, stake):
        self.browser.find_element(By.CSS_SELECTOR, '#betslip-bottom-betslip > span.l').click()
        browserCode = self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-container > div.l-betslip-mobile.l-mobile.show.small > div > div.code > div.code-input > input[type=text]')
        browserCode.send_keys(code)
        self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-container > div.l-betslip-mobile.l-mobile.show.small > div > div.code > button').click()