import time
import logging
from Base.base_driver import BaseDriver
from selenium.webdriver.common.by import By
from Utilities.utils import Utils


class SearchFlightsResults(BaseDriver):
    log = Utils.custom_logger(logLevel=logging.WARNING)
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    #locators
    FILTER_BY_1_STOP_ICON="//p[@class='font-lightgrey bold'][normalize-space()='1']"
    FILTER_BY_2_STOP_ICON="//p[@class='font-lightgrey bold'][normalize-space()='2']"
    FILTER_BY_NON_STOP_ICON="//p[@class='font-lightgrey bold'][normalize-space()='0']"
    SEARCH_FLIGHT_RESULTS="//span[contains(text(),'Non Stop') or contains(text(),'1 Stop') or contains(text(),'2 Stop')]"

    def get_filter_by_one_stop_icon(self):
        return self.driver.find_element(By.XPATH,self.FILTER_BY_1_STOP_ICON)

    def get_filter_by_two_stop_icon(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_2_STOP_ICON)

    def get_filter_by_non_stop_icon(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_NON_STOP_ICON)

    def get_search_flight_results(self):
        return self.waits_presence_of_all_elements(By.XPATH,"//span[contains(text(),'Non Stop') or contains(text(),'1 Stop') or contains(text(),'2 Stop')]")

    def filter_flights_by_stop(self,by_stop):
        if by_stop == "1 Stop":
            self.get_filter_by_one_stop_icon().click()
            self.log.warning("Selected flights with 1 Stop")
            time.sleep(4)
        elif by_stop == "2 Stops":
            self.get_filter_by_two_stop_icon().click()
            self.log.warning("Selected flights with 2 Stop")
            time.sleep(4)
        elif by_stop == "Non Stop":
            self.get_filter_by_non_stop_icon().click()
            self.log.warning("Selected non stop flights ")
            time.sleep(4)
        else:
            self.log.warning("Please provide valid filter option")



