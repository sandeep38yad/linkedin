from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from testCases.conftest import ignore_company_list
from utilities.db_insert import db_ops
import google.generativeai as genai
import time
from datetime import datetime
import re
# import gzip
# from bson import Binary

logger = LogGen.loggen('naukri_automation')


class jobs:
    job_section_url = ReadConfig.get_jobsection_url()
    top_pick_path = ReadConfig.get_top_job_picks_xpath()
    job_search_bar_xpath = ReadConfig.get_job_search_bar_xpath()
    date_filter = ReadConfig.get_date_filter_xpath()
    allfilter = ReadConfig.get_allfilter_xpath()
    one_day_xpath = ReadConfig.get_24_hourxpath()
    submit_oneday = ReadConfig.get_submit_one_day_xpath()
    jobcount_xpath = ReadConfig.get_jobcount_xpath()
    alljobsxpath = ReadConfig.get_all_jobs_xpath()

    def __init__(self, driver):
        self.driver = driver
        self.complete_job_details = []

    def open_job_page(self):
        try:
            self.driver.get(self.job_section_url)
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, self.top_pick_path))
            )
            return element.text

        except Exception as e:
            print(f'Error in open_job_page: {str(e)}')
            return False

    def add_one_day_filter(self):
        try:
            old_url = self.driver.current_url
            # temp = old_url.split("&")
            # temp[0] = "https://www.linkedin.com/jobs/search/?"
            # new_url = "&".join(temp) + "&f_TPR=r86400"
            new_url = old_url + "&f_TPR=r86400"
            self.driver.get(new_url)

        except Exception as e:
            print(f'add_one_day_filter: {str(e)}')

    def send_keywords_in_searchbar(self, keywords):
        try:
            # for keyword in keywords:
            self.driver.find_element(By.XPATH, self.job_search_bar_xpath).send_keys(keywords)
            self.driver.implicitly_wait(10)
            self.driver.find_element(By.XPATH, self.job_search_bar_xpath).send_keys(Keys.ENTER)
            time.sleep(5)
            self.add_one_day_filter()
            jobcount = self.driver.find_element(By.XPATH, self.jobcount_xpath).text.split(" ")[0]
            jobcount = jobcount.replace(",", "")
            return int(jobcount)

        except Exception as e:
            print(f'Error in send_keywords_in_searchbar: {str(e)}')
            logger.error(f'Error in send_keywords_in_searchbar: {str(e)}')


    def get_company_name(self):
        try:
            company = self.driver.find_element(By.XPATH, self.companyName_xpath).text
            return company
        except Exception as e:
            print(f'Error in get_company_name: {str(e)}')
            return False

    def check_direct_apply(self,title):
        try:
            qa_titles = ReadConfig.get_title_keywords('qa').split(",")
            pattern = '|'.join(qa_titles)
            if re.search(pattern, title, re.IGNORECASE):
                self.driver.find_element(By.XPATH, self.direct_apply_xpath).click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, self.chatbot_close_xpath).click()
        except Exception as e:
            pass
    def get_apply_link(self, title):
        try:
            self.driver.find_element(By.XPATH, self.apply_xpath).click()
            WebDriverWait(self.driver, 3).until(
                EC.new_window_is_opened(self.driver.window_handles)
            )
            # WebDriverWait(self.driver, 10).until(EC.new_window_is_opened(self.driver.window_handles))
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(0.5)
            applyURL = self.driver.current_url
            if self.driver.window_handles[-1] != self.driver.window_handles[0]:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            return applyURL

        except Exception as e:
            print(f'Error in get_apply_link: {str(e)}')
            # self.check_direct_apply(title)
            return "Not Found"

    def traversed(self, job, jobno):
        try:
            joblink = job.find_elements(By.XPATH, '//a[@class="title "]') #self.job_link_xpath)
            line = joblink[jobno].get_attribute('href')
            title = joblink[jobno].get_attribute('title')
            with open('./testCases/traversed.txt', 'r', encoding='utf-8') as f1:
                lines = f1.readlines()
            lines = {url.split()[2] for url in lines}
            if line in lines:
                print(f'Already traversed: {line}')
                return True
            if line not in lines:
                companies = ignore_company_list()
                pattern = '|'.join(companies)
                if re.search(pattern, line, re.IGNORECASE):
                    print(f'Mass recruiter so ignoring.....')
                    return True

            qa_titles = ReadConfig.get_title_keywords('qa').split(",")
            pattern = '|'.join(qa_titles)
            if re.search(pattern, title, re.IGNORECASE):
                current_time = datetime.now()
                # with open('./testCases/traversed.txt', 'a+', encoding='utf-8') as f1:
                #     print(str(current_time) + "  " + line, file=f1)
                return False
            else:
                print("Other department job so skipping......")
                return True

        except Exception as e:
            print(f'Error in traversed:{str(e)}')
            return False

    def get_full_detail(self):
        try:
            full_detail = self.driver.find_element(By.XPATH, ReadConfig.get_full_job_detail_xpath())
            # title_xpath = ReadConfig.get_title_xpath()
            # title = full_detail.find_element(By.XPATH, title_xpath)
            return full_detail.text

        except Exception as e:
            print(f'Error in getTitle: {str(e)}')
            return False

    def getLocation(self, element):
        try:
            full_detail = self.driver.find_element(By.XPATH, self.full_job_detail)
            loc = full_detail.find_element(By.XPATH, ReadConfig.get_loc_xpath())
            print("loc:", loc.text)
            return loc.text
        except Exception as e:
            print(f'Error in getLocation: {str(e)}')
            return False

    def get_company_name(self, element):
        try:
            name = element.find_element(By.XPATH, ReadConfig.getcompany_xpath())
            print("company:", name.text)

        except Exception as e:
            print(f'Error in get_company_name: {str(e)}')

    def get_temp_url(self, i):
        try:
            print("========JobNo.======:", i)
            # element = (self.driver.find_elements(By.XPATH, self.alljobsxpath))[i]
            element = (self.driver.find_elements(By.XPATH, '//a[contains(@href, "/jobs/view/")]'))[i]
            # name = element.find_element(By.XPATH, ReadConfig.get_temp_url_xpath())
            url = element.get_attribute('href')
            return url

        except Exception as e:
            print(f'Error in get_temp_url: {str(e)}')
            return None

    def get_experience(self, jd):
        try:
            genai.configure(api_key=ReadConfig.get_api_key())
            model = genai.GenerativeModel('gemini-pro')
            # model = genai.GenerativeModel('text - davinci - 003')
            response = model.generate_content(f"Analyze the given job description and give me just "
                                              f"one thing as output in float type 1. what is the Overall experience"
                                              f" required by a candidate to be eligible this job ."
                                              f"If no information is given regarding experience in the job description"
                                              f"then provide 0 as output. If experience range is given then analyze and"
                                              f"give minimum experience(not the average) required for this job as output. Job Description:{jd}")

            result = response.text
            return float(result)

        except Exception as e:
            print(f"An error occurred in get_experience: {e}")



    def check_category(self, title):
        try:
            qa_titles = ReadConfig.get_title_keywords('qa').split(",")
            qa_pattern = '|'.join(qa_titles)
            dev_title = ReadConfig.get_title_keywords('developer').split(",")
            dev_pattern = '|'.join(dev_title)
            ops_title = ReadConfig.get_title_keywords('devops').split(",")
            ops_pattern = '|'.join(ops_title)
            intern_title = ReadConfig.get_title_keywords('intern').split(",")
            intern_pattern = '|'.join(intern_title)

            if re.search(intern_pattern, title, re.IGNORECASE):
                print("Intern job")
                return "intern"

            elif re.search(qa_pattern, title, re.IGNORECASE):
                print("QA job")
                return "qa"

            elif re.search(ops_pattern, title, re.IGNORECASE):
                print("Ops job")
                return "devops"

            elif re.search(dev_pattern, title, re.IGNORECASE):
                print("Dev job")
                return "developer"

            print("No matching category")
            return False

        except Exception as e:
            print(f'Error in check_category: {str(e)}')
            return False

    def insert_doc_in_db(self, title, min_exp, company, loc, apply_link, full_jd):
        try:
            if not db_ops.check_availability("main", {'apply_link': apply_link}):
                if title and min_exp and company and apply_link:
                    document = {}
                    document['company'] = company
                    document['title'] = title
                    document['apply_link'] = apply_link
                    document['location'] = loc.split("sandeep")
                    # compressed_jd = gzip.compress(full_jd.encode('utf-8'))
                    # document['full_jd'] = Binary(compressed_jd)
                    document['full_jd'] = full_jd
                    document['min_exp'] = min_exp
                    document['time'] = datetime.now()
                    document['portal'] = 'linkedin'
                    document['category'] = self.check_category(title)
                    db_ops.insertion("main", document)
                    print(f'{company} successfully inserted')
            else:
                print(f'{apply_link} available in DB')
        except Exception as e:
            print(f'Error in insert_doc_in_db: {str(e)}')

    def insert_company_details(self, company, follower, industry):
        try:
            if not db_ops.check_availability("company_collection", {'company': company.lower()}):
                if company and follower and industry:
                    document = {}
                    document['company'] = company.lower()
                    document['industry'] = industry.lower()
                    document['follower'] = int(follower)
                    db_ops.insertion("company_collection", document)
        except Exception as e:
            print(f'Error in insert_company_details: {str(e)}')

    def get_apply_link(self):
        try:
            apply_button = self.driver.find_element(By.XPATH, ReadConfig.get_apply_xpath())
            if 'easy' not in apply_button.text.lower():
                apply_button.click()
                try:
                    self.driver.find_element(By.XPATH, ReadConfig.get_continue_xpath()).click()
                except:
                    pass
                try:
                    self.driver.find_element(By.XPATH, ReadConfig.get_continue_applying_xpath()).click()
                except:
                    pass
                # time.sleep(3)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                apply_url = self.driver.current_url
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                return apply_url
            else:
                return False

        except Exception as e:
            # self.driver.switch_to.window(self.driver.window_handles[0])
            print(f'Error in get_apply_link: {str(e)}')

    def get_full_jd(self, full_detail):
        try:

            genai.configure(api_key=ReadConfig.get_api_key())
            model = genai.GenerativeModel('gemini-pro')
            # model = genai.GenerativeModel('text - davinci - 003')
            response = model.generate_content(f"Summarize the given job description in very short only with key skills "
                                              f"required for this job. I want the response in this format: Key Skills:...."
                                              f" Job Description:{full_detail}")

            result = response.text
            return result

        except Exception as e:
            print(f"Error in get_full_jd: {str(e)}")



    def check_mass_recruiter(self, company):
        try:
            companies = ignore_company_list()
            # pattern = '|'.join(companies)
            pattern = '|'.join(re.escape(c) for c in companies)
            if re.search(pattern, company, re.IGNORECASE):
                print(f'Mass recruiter so ignoring.....')
                return True
            return False
        except Exception as e:
            print(f'Error in check_mass_recruiter:{str(e)}')

    def find_all_25_jobs(self, category, key, count):
        try:
            i = 0
            # job_traversed = 0
            while i < 25:
                try:
                    print(f'Job No. {i+1} | {key}')
                    each_job = self.driver.find_elements(By.XPATH, self.alljobsxpath)[i]
                    # self.driver.implicitly_wait(10)  ##### Check this====================
                    each_job.click()
                    time.sleep(2)
                    full_detail = self.get_full_detail()
                    # url = self.get_temp_url(i)
                    i += 1
                    full = full_detail.splitlines()
                    # print("====================line_count:", len(full))
                    print("===Company:", full[0])
                    company = full[0]
                    print("===JobTitle:", full[3])
                    title = full[3]

                    ct = self.check_category(title)
                    if ct != category or not ct:
                        print("Other department job")
                        continue
                    if self.check_mass_recruiter(company):
                        continue

                    apply_link = self.get_apply_link()
                    if apply_link:
                        apply_link = apply_link.split('?')[0]
                        print("======applyLink", apply_link)
                        if 'internshala' in apply_link.lower():
                            continue

                    if db_ops.check_availability("main", {'apply_link': apply_link}):
                        print("Duplicate")
                        continue

                    jd = self.get_full_jd(full_detail)
                    print("jd===========================\n", jd)
                    # min_exp = self.get_experience(jd.splitlines())
                    if category.lower() == 'intern':
                        min_exp = 0
                    else:
                        min_exp = self.get_experience(full_detail)
                    print(min_exp)
                    if db_ops.check_availability("main", {'company': company, 'title': title, 'min_exp': min_exp}):
                        print("Already traversed....")
                        continue
                    loc = (full[4].split("·")[0]).split(",")[0]
                    print("===Location:", loc)
                    follower = re.compile(r'(followers)', re.IGNORECASE)
                    industry_full_line = re.compile(r'(?=.*employees)(?=.*on Linkedin)', re.IGNORECASE)
                    industry_pattern = re.compile(r'employees.*on LinkedIn')
                    follower_count = None
                    industry = None
                    for line in full:
                        if follower.search(line):
                            f = line.replace(",", "")
                            follower_count = (f.split(" ")[0])
                            print("=====Follower:", follower_count)
                        # if industry_pattern.search(line):
                        if industry_pattern.search(line):
                            ind_match = re.match(r"^(.*?)\s\d", line)
                            if ind_match:
                                industry = ind_match.group(1).strip()
                            #     print(industry)
                            # industry = line
                            print("=====Industry:", industry)

                    if category.lower() != 'intern':
                        if industry and follower_count and int(follower_count) > 5000:
                            self.insert_company_details(company, follower_count, industry)
                            if industry and 'consulting' not in industry.lower() and 'e-learning' not in industry.lower():
                                self.insert_doc_in_db(title, min_exp, company, loc, apply_link, jd)
                    else:
                        if industry and follower_count and apply_link and 'internshala' not in apply_link.lower():
                            self.insert_company_details(company, follower_count, industry)
                            if industry and 'consulting' not in industry.lower() and 'e-learning' not in industry.lower():
                                self.insert_doc_in_db(title, min_exp, company, loc, apply_link, jd)

                except StaleElementReferenceException:
                    print("Found stale elements.. retrying")
                    i -= 1
                    continue

        except Exception as e:
            print(f'Error in find_all_25_jobs:{str(e)}')

    def find_no_of_jobs(self, category, key):
        try:
            key = key.replace(" ", "%20")
            new_page = ReadConfig.get_next_page_url(category).replace("unknown", key)
            self.driver.get(new_page + '0')
            self.driver.implicitly_wait(10)
            jobcount = self.driver.find_element(By.XPATH, self.jobcount_xpath).text.split(" ")[0]
            jobcount = jobcount.replace(",", "")
            return int(jobcount)
        except Exception as e:
            print(f'Error in find_no_of_jobs: {str(e)}')

    def collect_details(self, category, key, count=0):
        try:

            for i in range(0, count, 25):
                key = key.replace(" ", "%20")
                new_page = ReadConfig.get_next_page_url(category).replace("unknown", key)
                self.driver.get(new_page + str(i))

                self.driver.implicitly_wait(5)
                self.find_all_25_jobs(category, key, count)

        except Exception as e:
            print(f'Error in collect_details: {str(e)}')


