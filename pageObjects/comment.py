from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities.customLogger import LogGen
import json
import google.generativeai as genai
from utilities.readProperties import ReadConfig


logger = LogGen.loggen('naukri_automation')


class AddComment:
    def __init__(self, driver):
        self.driver = driver


    def open_feed(self):
        try:
            self.driver.get("https://www.linkedin.com/feed/")
            wait = WebDriverWait(self.driver, 30)
            all_posts = wait.until(EC.presence_of_element_located(By.XPATH, '//div[@class="feed-shared-update-v2__control-menu-container display-flex flex-column flex-grow-1"]'))
            if all_posts:
                posts = self.driver.find_elements(By.XPATH, '//div[@class="feed-shared-update-v2__control-menu-container display-flex flex-column flex-grow-1"]')
                return len(posts)
        except Exception as e:
            print(f'Error in open_feed:{str(e)}')


    def get_all_posts(self):
        try:
            wait = WebDriverWait(self.driver, 30)
            all_posts = wait.until(EC.presence_of_element_located(By.XPATH, '//div[@class="feed-shared-update-v2__control-menu-container display-flex flex-column flex-grow-1"]'))
            if all_posts:
                posts = self.driver.find_elements(By.XPATH,
                                              '//div[@class="feed-shared-update-v2__control-menu-container display-flex flex-column flex-grow-1"]')
                return posts
            return False
        except Exception as e:
            print(f'Error in get_all_post')

    def get_content(self, post):
        try:
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.presence_of_element_located(By.XPATH, 'class="feed-shared-update-v2__description-wrapper"'))
            content = self.driver.find_element(By.XPATH, '//div[@class="feed-shared-update-v2__description-wrapper"]')
            return content

        except Exception as e:
            print(f'Error in get_content:{str(e)}')

    def already_analyzed(self, content):
        try:
            filename = "traversed.json"
            try:
                with open(filename, "r") as file:
                    traversed_paragraphs = set(json.load(file))
            except (FileNotFoundError, json.JSONDecodeError):
                traversed_paragraphs = set()

            if content in traversed_paragraphs:
                return True
            else:
                return False
        except Exception as e:
            print(f'Error in already_analyzed:{str(e)}')

    def get_analyzed_content(self, content):
        try:
            genai.configure(api_key=ReadConfig.get_comment_api_key())
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Below given is a linkedin post written by user."
                                              "If it is a educational post in QA or SDET or Testing related domain"
                                              "then analyze the post and provide me a comment for that post of not more"
                                              "than 2 lines that I can write on this post. If the post is not "
                                              "educational just promoting anything or it is for job openings "
                                              "then simple provide False as the output nothing else"
                                              f"This is the post: {content}")

            result = response.text
        except Exception as e:
            print(f'Error in get_analyzed_content:{str(e)}')