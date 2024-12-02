from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageObjects.comment import AddComment
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities.db_insert import db_ops
import pytest
import time
from pageObjects.CompanyDetails import Details

logger = LogGen.loggen('linkedin_automation')


class Test_004_Comment:

    def test_open_feed(self, browser_setup):
        logger.info("*********************Test_004_PostComment**************************************")
        logger.info("Opening feed")
        self.driver = browser_setup
        self.c = AddComment(self.driver)
        no_of_posts = self.c.open_feed()
        print(f"Total posts on feed: {no_of_posts}")
        if no_of_posts > 0:
            logger.info("open_feed test PASSED")
            assert True
        else:
            logger.info("open_feed test FAILED")
            assert False

    def test_post_analyze(self, browser_setup):
        try:
            logger.info("*********************Test_004_PostComment**************************************")
            logger.info("post_analyzing")
            self.driver = browser_setup
            self.c = AddComment(self.driver)
            posts = self.c.get_all_posts()
            if posts:
                for post in posts:
                    content = self.c.get_content(post)
                    print("Content:", content)
                    if self.c.already_analyzed(content):
                        continue
                    analyzed_content = self.c.get_analyzed_content(content)
                    print(analyzed_content, "\n")
                    # self.c.post_comment(analyzed_content)
                    # self.c.mark_analyzed()

        except Exception as e:
            print(f'Error in post_analyzer:{str(e)}')

