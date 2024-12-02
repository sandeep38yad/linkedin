from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utilities.readProperties import ReadConfig
from utilities.db_insert import db_ops, ignore_collection

import time
import json

class Details:
    search_bar_xpath = ReadConfig.getlinkedin_search_xpath()
    filter_xpath = ReadConfig.get_filter_xpath()
    about_xpath = ReadConfig.getabout_xpath()
    all_company_xpath = ReadConfig.get_allcompany_xpath()
    industry_xpath = ReadConfig.get_industry_xpath()
    follower_xpath = ReadConfig.get_follower_xpath()
    no_result_found = ReadConfig.get_no_company_xpath()

    def __init__(self, driver):
        self.driver = driver

    def check_company_details(self, company_name, company_element):
        try:

            result = {"company": company_name.lower()}
            company_name = company_name.lower()
            names = company_name.split(" ")
            if len(names) > 3:
                names_to_check = " ".join(names[0:2])
            else:
                names_to_check = " ".join(names)

            print("Checking company details", names_to_check)
            if names_to_check in company_element.text.lower():
                result["industry"] = self.driver.find_element(By.XPATH, self.industry_xpath).text.split(" • ")[0]
                follower = self.driver.find_element(By.XPATH, self.follower_xpath).text.split(" ")[0]
                if "M" in follower:
                    total_followers = int(follower[:-1]) * 1000000
                elif "K" in follower:
                    total_followers = int(follower[:-1]) * 1000
                elif "M" not in follower and "K" not in follower:
                    total_followers = int(follower)

                result["follower"] = total_followers

                print(result)
                return result
            else:
                db_ops.delete_doc("company_collection", {'company': company_name.lower()})
                print(f'Deleted {company_name} from company collection')
                if not ignore_collection.find_one({'company': company_name.lower()}):
                    ignore_collection.insert_one({'company': company_name.lower()})
                return False
        except Exception as e:
            print(f'Error in check_company_details: {str(e)}')

    def apply_company_filter(self, company):
        try:
            company = company.replace(" ", "%20")
            url = f'https://www.linkedin.com/search/results/companies/?keywords={company}&origin=SWITCH_SEARCH_VERTICAL&sid=ggs'
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            # filters = self.driver.find_elements(By.XPATH, self.filter_xpath)
            # for f in filters:
            #     if 'companies' in f.text.lower():
            #         f.click()
            #         break
        except Exception as e:
            print(f'Error in apply_company_filter:{str(e)}')

    def no_result_found(self):
        try:
            if "no results" in self.driver.find_element(By.XPATH, self.no_result_found).text.lower():
                print("Not found...")
                return True
        except Exception as e:
            return False
            # print(f'Error in no_result_found:{str(e)}')

    # def fetch_company_details(self, company):
    #     try:
    #         company = company.replace(" ", "%20")
    #         url = f'https://www.linkedin.com/search/results/companies/?keywords={company}&origin=SWITCH_SEARCH_VERTICAL&sid=ggs'
    #         self.driver.get(url)
    #
    #     except Exception as e:
    #         print(f'Error in fetch_company_details:{str(e)}')
    def OpenCompanyPage(self):
        company_list = db_ops.company_without_details()
        search_box = self.driver.find_element(By.XPATH, self.search_bar_xpath)
        if len(company_list[0].split(" ")[0]) < 4:
            company_to_search = " ".join((company_list[0].split(" "))[0:2])
        else:
            company_to_search = company_list[0].split(" ")[0]

        # search_box.send_keys(company_to_search)
        # search_box.send_keys(Keys.RETURN)
        # time.sleep(1)
        self.apply_company_filter(company_to_search)
        if self.no_result_found():
            ignore_collection.insert_one({'company': company_list[0].lower()})
        try:
            # json_result = []
            all_companies = self.driver.find_elements(By.XPATH, ReadConfig.get_allcompany_xpath())
            if len(all_companies) > 0:
                result = self.check_company_details(company_list[0], all_companies[0])
                if result:
                    db_ops.insert_company_details(result)
                    # json_result.append(result)

            if len(company_list) > 1:
                for i in range(1, len(company_list)):
                    try:
                        # search_box = self.driver.find_element(By.XPATH, self.search_bar_xpath)
                        # search_box.clear()
                        if len(company_list[i].split(" ")[0]) < 4:
                            company_to_search = " ".join((company_list[i].split(" "))[0:2])
                        else:
                            company_to_search = company_list[i].split(" ")[0]
                        # search_box.send_keys(company_to_search)
                        # search_box.send_keys(Keys.RETURN)
                        # time.sleep(1)
                        self.apply_company_filter(company_to_search)
                        if self.no_result_found():
                            ignore_collection.insert_one({'company': company_list[i].lower()})
                            continue
                        companies = self.driver.find_elements(By.XPATH, ReadConfig.get_allcompany_xpath())
                        if len(companies) > 0:
                            result2 = self.check_company_details(company_list[i], companies[0])
                            if result2:
                                # json_result.append(result2)
                                db_ops.insert_company_details(result2)
                    except Exception as e:
                        print(f'Error in loop of OpenCompanyPage:{str(e)}')

            # with open(r'./testCases/companydetails.json', 'w', encoding='utf-8') as file:
            #     json.dump(json_result, file, indent=4)

        except Exception as e:
            print(f'Error in OpenCompanyPage:{str(e)}')

    def check_details(self):
        all_details = self.driver.find_element(By.XPATH, ReadConfig.get_companyinfo_xpath())
        for detail in all_details:
            print(detail.text)
