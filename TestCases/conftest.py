import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
import time



@pytest.fixture(autouse=True)  # provide this fixture at class level
def setup(request,browser,url):   # request is  to connect both conftest.py  and test_searchflights.py files
    if browser == "chrome":
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser == "edge":
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    driver.get(url)
    driver.maximize_window()
    request.cls.driver = driver  # intiated driver should be at class level and given to classes which are requesting
    yield
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--url")
@pytest.fixture(scope="class",autouse=True)
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="class",autouse=True)
def url(request):
    return request.config.getoption("--url")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html=item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        # always add url to report
        extras.append(pytest_html.extras.url("http://www.nsrtechnologies.in"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure

             report_directory=os.path.dirname(item.config.option.htmlpath)
            # file_name=str(int(round(time.time()*1000)))+".png"
             file_name=report.nodeid.replace("::","_")+".png"
             destinationFile=os.path.join(report_directory,file_name)
             driver = item.cls.driver
             driver.save_screenshot(destinationFile)
             if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:300px;height=200px" onclick="window.open(this.src)" align="right"/></div>'%file_name
             extras.append(pytest_html.extras.html(html))
        report.extras=extras


def pytest_html_report_title(report):
    report.title=" NSR Automation framework Report"








