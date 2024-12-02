from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities.db_insert import db_ops
import pytest
import time
from pageObjects.CompanyDetails import Details

logger = LogGen.loggen('linkedin_automation')

#@pytest.mark.usefixtures("browser_setup")
class Test_001_Login:
    base_url = ReadConfig.getbase_url()
    username = ReadConfig.getusername()
    password = ReadConfig.getpassword()
    username_xpath = ReadConfig.getuserxpath()
    pass_xpath = ReadConfig.getpassxpath()

    def test_login_page_webelements(self, browser_setup):
        try:
            logger.info("*********************Test_001_Login**************************************")
            logger.info("Verifying login page web elements ")
            self.driver = browser_setup
            self.lp = LoginPage(self.driver)
            if self.lp.open_login_page():
                print("Web Elements are present")
                assert True
            else:
                print("Missing Web Elements")
                assert False

        except Exception as e:
            print(f'Error in test_login_page_webelements:{str(e)}')
            assert False


    def test_login(self,browser_setup):
        try:
            logger.info("*********************Test_001_Login**************************************")
            logger.info("Verifying Login ")
            time.sleep(2)
            self.driver = browser_setup
            self.lp = LoginPage(self.driver)
            self.lp.setUserName(self.username)
            self.lp.setPassword(self.password)
            self.lp.submit()
            time.sleep(2)
            text_value = self.driver.find_element(By.XPATH, ReadConfig.getuser_fullname()).text
            if ReadConfig.getuser_expected_name().lower() in text_value.lower():
                print("Login successful!")
                logger.info("Login test PASSED")
                #self.lp.logout()
                assert True
            else:
                print(text_value)
                print("Login failed")
                print(self.driver.title.lower())
                self.driver.save_screenshot(".\\screenshots\\" + "test_login.png")
                logger.info("Login test FAILED")
                assert False

        except Exception as e:
            logger.error(f"{str(e)}")




