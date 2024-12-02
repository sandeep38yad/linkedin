import pytest
from selenium import webdriver
from pytest_metadata.plugin import metadata_key
from pymongo import MongoClient
from utilities.readProperties import ReadConfig

#@pytest.fixture(scope="class")
@pytest.fixture(scope="session")
def browser_setup(request, browser='firefox'):
    if (browser.lower() == 'chrome'):
        driver = webdriver.Chrome()
        print("Launching Chrome")
    if (browser.lower() == 'firefox'):
        driver = webdriver.Firefox()
        print("Launching Firefox")
    if (browser.lower() == 'internet explorer'):
        driver = webdriver.Ie()
        print("Launching Internet Explorer")
    #request.cls.driver = driver
    yield driver
    #driver.quit()

def ignore_company_list():
    try:
        result = []
        client = MongoClient(ReadConfig.get_db_details('url'))
        db = client[ReadConfig.get_db_details('db')]
        collection = db[ReadConfig.get_db_details('ignorelist')]
        cursor = collection.find()
        for element in cursor:
            result.append(element['company'])
        return result
    except Exception as e:
        print(f'Error in ignore_company_list:{str(e)}')

def pytest_addoption(parser):
    parser.addoption("--browser")  # This will get value from cli


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")  #This will return the browser value to setup method

def pytest_html_report_title(report):
    report.title = "Naukri.com portal test report"

# It is hook for Adding Environment info to HTML Report
def pytest_configure(config):
    config.stash[metadata_key]["Project"] = "naukri.com"
    config.stash[metadata_key]["Module"] = "User"
    config.stash[metadata_key]["Tester"] = "Sandeep"

# It is hook for delete/Modify Environment info to HTML Report
#@pytest.mark.optionalhook
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)