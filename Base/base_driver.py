import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
class BaseDriver:
    def __init__(self, driver):
        self.driver = driver


    def page_scroll(self):
        pageLength = self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight);var pageLength=document.body.scrollHeight;return pageLength;")
        match = False
        while (match == False):
            lastCount = pageLength
            time.sleep(3)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight);var pageLength=document.body.scrollHeight;return pageLength;")
            if lastCount == pageLength:
                match = True
            time.sleep(5)



    def waits_presence_of_all_elements(self,locator_type,locator):
        wait = WebDriverWait(self.driver, 20)
        list_of_all_elements=wait.until(EC.presence_of_all_elements_located((locator_type,locator)))
        return list_of_all_elements

    def waits_until_element_is_clickable(self,locator_type,locator):
        wait = WebDriverWait(self.driver, 30)
        element=wait.until(EC.element_to_be_clickable((locator_type,locator)))
        return element




