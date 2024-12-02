from utilities.customLogger import LogGen
from utilities.db_insert import db_ops
from pageObjects.CompanyDetails import Details
import pytest
import time

logger = LogGen.loggen('linkedin_automation')

class Test_002_Company:

    def test_company_details(self, browser_setup):
        try:
            logger.info("*********************Test_002_Company**************************************")
            logger.info("Collecting Company details")
            self.driver = browser_setup
            self.Dt = Details(self.driver)
            self.Dt.OpenCompanyPage()
            # db_ops.insert_company_details()
            assert True

        except Exception as e:
            print(f'Error in test_company_details:{str(e)}')
            assert False