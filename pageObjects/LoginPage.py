from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utilities.readProperties import ReadConfig
import time
class LoginPage:
    username_xpath = ReadConfig.getuserxpath()
    pass_xpath = ReadConfig.getpassxpath()
    submit_xpath = ReadConfig.getsubmitxpath()
    bar_xpath = ReadConfig.getbarxpath()
    logout_xpath = ReadConfig.getlogoutxpath()
    base_url = ReadConfig.getbase_url()
    # sing_in_button = ReadConfig.getsignin_xpath()

    def __init__(self, driver):
        self.driver = driver

    def open_login_page(self):
        try:
            self.driver.get(self.base_url)
            self.driver.implicitly_wait(10)
            # self.driver.find_element(By.XPATH, self.sing_in_button)
            element_user = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.username_xpath)))
            element_pass = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.pass_xpath)))

            if element_user and element_pass:
                return True
            else:
                return False
        except Exception as e:
            print(f'Error in open_login_page:{str(e)}')

    def setUserName(self, username):
        self.driver.find_element(By.XPATH, self.username_xpath).send_keys(username)

    def setPassword(self, password):
        self.driver.find_element(By.XPATH, self.pass_xpath).send_keys(password)

    def submit(self):
        self.driver.find_element(By.XPATH, self.submit_xpath).click()
    def logout(self):
        self.driver.find_element(By.XPATH, self.bar_xpath).click()
        self.driver.find_element(By.XPATH, self.logout_xpath).click()
        print("Clicked logout")
        time.sleep(3)
