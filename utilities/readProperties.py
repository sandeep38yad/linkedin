import configparser

config = configparser.RawConfigParser()
config.read(".\\Configurations\\config.ini")

class ReadConfig:

    @staticmethod
    def get_api_key():
        api = config.get('common info', 'api_key')
        return api

    @staticmethod
    def get_comment_api_key():
        api = config.get('common info', 'comment_api_key')
        return api

    @staticmethod
    def getsignin_xpath():
        signin_button = config.get('common info', 'signin_xpath')
        return signin_button

    @staticmethod
    def getuser_fullname():
        name = config.get('common info', 'NAME_xpath')
        return name

    @staticmethod
    def getuser_expected_name():
        realname = config.get('common info', 'NAME_xpath')
        return realname

    @staticmethod
    def getbase_url():
        url = config.get('common info', 'base_url')
        return url

    @staticmethod
    def getusername():
        user = config.get('common info', 'username')
        return user

    @staticmethod
    def getpassword():
        password = config.get('common info', 'password')
        return password

    @staticmethod
    def getuserxpath():
        uxpath = config.get('common info', 'username_xpath')
        return uxpath

    @staticmethod
    def getpassxpath():
        pxpath = config.get('common info', 'pass_xpath')
        return pxpath

    @staticmethod
    def getsubmitxpath():
        sxpath = config.get('common info', 'submit_xpath')
        return sxpath

    @staticmethod
    def getbarxpath():
        bxpath = config.get('common info', 'bar_xpath')
        return bxpath

    @staticmethod
    def getlogoutxpath():
        lxpath = config.get('common info', 'logout_xpath')
        return lxpath

    @staticmethod
    def getlinkedin_search_xpath():
        search_bar_xpath = config.get('companyDetails', 'linkedin_search_xpath')
        return search_bar_xpath

    @staticmethod
    def get_filter_xpath():
        filter_xpath = config.get('companyDetails', 'filter_xpath')
        return filter_xpath


    @staticmethod
    def get_no_company_xpath():
        no_company_xpath = config.get('companyDetails', 'no_company_xpath')
        return no_company_xpath

    @staticmethod
    def get_allcompany_xpath():
        company_xpath = config.get('companyDetails', 'companylist_xpath')
        return company_xpath

    @staticmethod
    def getabout_xpath():
        about = config.get('companyDetails', 'about_xpath')
        return about

    @staticmethod
    def get_companyinfo_xpath():
        info = config.get('companyDetails', 'company_info_xpath')
        return info

    @staticmethod
    def get_industry_xpath():
        industry_xpath = config.get('companyDetails', 'industry_xpath')
        return industry_xpath

    @staticmethod
    def get_follower_xpath():
        follower_xpath = config.get('companyDetails', 'follower_xpath')
        return follower_xpath

    @staticmethod
    def get_title_keywords(department):
        qatitles = config.get('jobsearch section', 'qa_titles')
        developertitles = config.get('jobsearch section', 'developer_titles')
        devopstitles = config.get('jobsearch section', 'devops_titles')
        interntitles = config.get('jobsearch section', 'intern_titles')
        if department == 'qa':
            return qatitles
        elif department == 'developer':
            return developertitles
        elif department == 'devops':
            return devopstitles
        elif department == 'intern':
            return interntitles

    @staticmethod
    def getkeyword(category):
        if category == 'qa':
            keyword = config.get('jobsearch section', 'keyword')
            return keyword
        elif category == 'developer':
            dev_keyword = config.get('jobsearch section', 'dev_keyword')
            return dev_keyword
        elif category == 'devops':
            ops_keyword = config.get('jobsearch section', 'ops_keyword')
            return ops_keyword
        elif category == 'intern':
            intern_keyword = config.get('jobsearch section', 'intern_keyword')
            return intern_keyword
    @staticmethod
    def get_jobsection_url():
        url = config.get('jobsearch section', 'job_url')
        return url

    @staticmethod
    def get_next_page_url(type):
        next_page = config.get('jobsearch section', 'next_page_url')
        if type == "intern":
            next_page = config.get('jobsearch section', 'intern_next_page_url')
        return next_page

    @staticmethod
    def get_top_job_picks_xpath():
        picks = config.get('jobsearch section', 'top_job_picks_xpath')
        return picks

    @staticmethod
    def get_job_search_bar_xpath():
        search_bar = config.get('jobsearch section', 'job_search_bar_xpath')
        return search_bar

    @staticmethod
    def get_date_filter_xpath():
        date_filter = config.get('jobsearch section', 'date_filter')
        return date_filter

    @staticmethod
    def get_allfilter_xpath():
        allfilter_xpath = config.get('jobsearch section', 'all_filter')
        return allfilter_xpath

    @staticmethod
    def get_24_hourxpath():
        one_day = config.get('jobsearch section', '24hourxpath')
        return one_day

    @staticmethod
    def get_submit_one_day_xpath():
        one_day = config.get('jobsearch section', '24hourxpath')
        return one_day

    @staticmethod
    def get_db_details(value):
        conn_string = config.get("db details", 'conn_string')
        db = config.get("db details", 'db')
        collection = config.get("db details", 'collection')
        ignore_collection = config.get("db details", 'ignoreCollection')
        company_collection = config.get("db details", 'companyCollection')
        if value == 'url':
            return conn_string
        elif value == 'db':
            return db
        elif value == 'ignorelist':
            return ignore_collection
        elif value == 'collection':
            return collection
        elif value == 'company':
            return company_collection


    @staticmethod
    def get_jobcount_xpath():
        count = config.get('jobdetail section', 'jobcount_xpath')
        return count

    @staticmethod
    def get_all_jobs_xpath():
        all_jobs = config.get('jobdetail section', 'all_jobs_xpath')
        return all_jobs

    @staticmethod
    def get_full_job_detail_xpath():
        job_detail = config.get('jobdetail section', 'full_job_detail_xpath')
        return job_detail

    @staticmethod
    def get_title_xpath():
        title = config.get('jobdetail section', 'title_xpath')
        return title

    @staticmethod
    def get_loc_xpath():
        loc = config.get('jobdetail section', 'loc_xpath')
        return loc

    @staticmethod
    def get_work_mode_xpath():
        work_mode = config.get('jobdetail section', 'work_mode_xpath')
        return work_mode

    @staticmethod
    def getcompany_xpath():
        company = config.get('jobdetail section', 'company')
        return company

    @staticmethod
    def get_temp_url_xpath():
        url = config.get('jobdetail section', 'temp_url')
        return url

    @staticmethod
    def get_full_jd_xpath():
        url = config.get('jobdetail section', 'full_jd')
        return url

    @staticmethod
    def get_apply_xpath():
        apply = config.get('jobdetail section', 'apply_xpath')
        return apply

    @staticmethod
    def get_continue_xpath():
        continue_xpath = config.get('jobdetail section', 'continue_xpath')
        return continue_xpath

    @staticmethod
    def get_continue_applying_xpath():
        continue_applying_xpath = config.get('jobdetail section', 'continue_applying_xpath')
        return continue_applying_xpath




