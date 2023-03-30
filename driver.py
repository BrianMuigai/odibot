from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver_py import binary_path
from selenium.webdriver.support import expected_conditions as EC
import time

class Driver():
    def __init__(self) -> None:
        self.report = []
        service_object = Service(binary_path)
        self.browser = webdriver.Chrome(service=service_object)

    def bet(self, phone, password, code, stake):
        self.__login(phone, password)
        self.__placeBet(code, stake)

    def timer(self, t) -> None:
         while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            t -= 1
        
    def __login(self, mPhone, mPass) -> None:
        self.mPhone = mPhone
        self.browser.get("https://odibets.com")
        print("Login Odibet...")
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
            self.report.append(msg)

    def logout(self):
        self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-header.rich.l-mobile > div.l-header-top > div > div.menu > i').click()
        self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-sidebar.l-mobile.show > div > div:nth-child(6) > ul > li > div').click()

        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mobile-web-login'))
            )
        except:
            msg = 'Could not log out user: '+self.mPhone
            self.report.append(msg)


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

        self.browser.find_element(By.CSS_SELECTOR, '#body > div.theme-1.l-page.l-mobile.t-light > div.l-page.l-mobile.theme-1.t-dark > div:nth-child(1) > div.l-container > div.l-betslip-mobile.l-mobile.show > div > div.bottom > div.bottom-cta > div > button').click()
        self.timer(5)


    def report(self):
        print('\n\n\n')
        print('-'*10)
        print('\n')
        
        for msg in self.report:
            print(msg)

        print('-'*10)
        print('\n')