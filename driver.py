from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import threading
import utils

class Driver(threading.Thread):
    def __init__(self, executablePath, options, lock) -> None:
        super().__init__()
        self.report = []
        self.lock = lock
        # service_object = Service(binary_path)
        # self.browser = webdriver.Chrome(service=service_object)
        self.browser = webdriver.Opera(executable_path=executablePath, options=options)

    def bet(self, phone, password, code, stake):
        self.__login(phone, password)
        try:
            self.__placeBet(code, stake)
        except:
            msg = 'Could not place bet '+code+' for user '+self.mPhone
            self.__addReport(phone, password, code, stake, 'BET', msg)

    def timer(self, t) -> None:
         while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            t -= 1
        
    def __login(self, mPhone, mPass) -> None:
        self.mPhone = mPhone
        self.password = mPass

        self.browser.get("https://odibets.com")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mobile-web-login'))
        )

        loginButton = self.browser.find_element(By.CSS_SELECTOR, '#mobile-web-login')
        loginButton.click()

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
            msg = 'Could not login user: '+ mPhone +' password: '+ mPass
            self.__addReport(mPhone, mPass, '', '', 'LOGIN', msg)

    def __placeBet(self, code, stake):
        self.browser.find_element(By.CSS_SELECTOR, '#betslip-bottom-betslip > span.l').click()
        browserCode = self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-container > div.l-betslip-mobile.l-mobile.show.small > div > div.code > div.code-input > input[type=text]')
        browserCode.send_keys(code)
        self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-container > div.l-betslip-mobile.l-mobile.show.small > div > div.code > button').click()
        
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-container > div.l-betslip-mobile.l-mobile.show.small > div > div.bottom > div.bottom-cta > div > button'))
        )
        self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-container > div.l-betslip-mobile.l-mobile.show.small > div > div.top > div.top-collapse > i').click()
        stakeBox = self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-container > div.l-betslip-mobile.l-mobile.show > div > div.bottom > div.bottom-stk > div.stk > div.stk-input > input[type=number]')
        stakeBox.clear()
        stakeBox.send_keys(stake)
        self.timer(2)

        def close(counter = 0):
            try:    
                self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-container > div.l-betslip-mobile.l-mobile.show > div > div.bottom > div.bottom-cta > div > button').click()
                self.timer(5)
                self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-modal-mobile.bet.l-mobile.show > div > div.cta > div.c.s > button').click()
                self.timer(5)
                print('\n')
                print('#'*50)

                print('Place Bet', code,' for ',self.mPhone)
                self.browser.close()
            except:
                counter += 1
                if counter < 3:
                    close(counter=counter)
                else:
                    msg = 'Could not place bet '+code+' for user '+self.mPhone
                    self.__addReport(self.mPhone, self.password, code, stake, 'BET', msg)

        close()

    def __addReport(self, username, password, booking_code, stake, error, errorMsg):
        data = {
            'username':username,
            'password':password,
            'booking_code':booking_code,
            'stake':stake,
            'error': error,
            'errorMsg':errorMsg
        }
        self.report.append(data)

    def saveReport(self):
        #todo handle concurency issue with threads
        if len(self.report) == 0:
            return
        with self.lock:
            with open('failed.csv', 'a') as file:
                writer = csv.writer(file)
                for data in self.report:
                    if not self.__exists(data['errorMsg']):
                        row = [data['username'], data['password'], data['booking_code'], data['stake'], data['error'], data['errorMsg']]
                        writer.writerow(row)
    
    def __exists(self, msg):
        with open('failed.csv') as file:
            next(file) #removes header
            reader = csv.reader(file)
            for row in reader:
                if row[5] == msg:
                    return True
                    
        return False