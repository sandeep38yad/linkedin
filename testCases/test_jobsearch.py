from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageObjects.jobsearch import jobs
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities.db_insert import insertDB
import pytest
import time
import json

logger = LogGen.loggen('linkedin_automation')

class Test_003_Jobsearch_Qa:
    # keywords = ReadConfig.get_title_keywords("qa").split(",")

    def test_open_job_page(self, browser_setup):
        logger.info("*********************Test_003_Jobsearch**************************************")
        logger.info("Checking opening of job page")
        self.driver = browser_setup
        self.jb = jobs(self.driver)
        result = self.jb.open_job_page()
        if result and "job picks" in result.lower():
            logger.info("Opening job page test  PASSED")
            assert True
        else:
            logger.info("job picks is not available on opening job page")
            print("job picks is not available on opening job page")

    # def test_job_availibility_qa(self, browser_setup):
    #     logger.info("*********************Test_003_Jobsearch**************************************")
    #     logger.info("Checking opening of job page for qa")
    #     self.driver = browser_setup
    #     self.jb = jobs(self.driver)
    #     keywords = ReadConfig.getkeyword("qa").split(",")
    #     for keyword in keywords:
    #         count = 0
    #         count = self.jb.send_keywords_in_searchbar(keyword)
    #         print(f'Total count {count}')
    #         # self.jb.job_count()
    #         self.jb.collect_details("qa", keyword, count)
    #         # result = self.jb.open_job_page()

    # def test_job_availibility_intern(self, browser_setup):
    #     logger.info("*********************Test_003_Jobsearch**************************************")
    #     logger.info("Checking opening of job page for internship")
    #     self.driver = browser_setup
    #     self.jb = jobs(self.driver)
    #     keywords = ReadConfig.getkeyword("intern").split(",")
    #     for keyword in keywords:
    #         count = 0
    #         # count = self.jb.send_keywords_in_searchbar(keyword)
    #         count = self.jb.find_no_of_jobs("intern", keyword)
    #         print(f'Total count {count}')
    #         self.jb.collect_details("intern", keyword, count)

    def test_job_availibility_dev(self, browser_setup):
        logger.info("*********************Test_003_Jobsearch**************************************")
        logger.info("Checking opening of job page for dev")
        self.driver = browser_setup
        self.jb = jobs(self.driver)
        keywords = ReadConfig.getkeyword("developer").split(",")
        for keyword in keywords:
            count = 0
            count = self.jb.send_keywords_in_searchbar(keyword)
            print(f'Total count {count}')
            # self.jb.job_count()
            self.jb.collect_details("developer", keyword, count)
    #
    # def test_job_availibility_devops(self, browser_setup):
    #     logger.info("*********************Test_003_Jobsearch**************************************")
    #     logger.info("Checking opening of job page for devops")
    #     self.driver = browser_setup
    #     self.jb = jobs(self.driver)
    #     keywords = ReadConfig.getkeyword("devops").split(",")
    #     for keyword in keywords:
    #         count = 0
    #         count = self.jb.send_keywords_in_searchbar(keyword)
    #         print(f'Total count {count}')
    #         # self.jb.job_count()
    #         self.jb.collect_details("devops", keyword, count)
