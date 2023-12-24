import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Base.base_driver import BaseDriver
from Pages.search_flights_results_page import SearchFlightsResults
from Utilities.utils import Utils


class launchPage(BaseDriver):
    log = Utils.custom_logger()
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    #locators
    DEPART_FROM_FIELD="//input[@id='BE_flight_origin_city']"
    GOING_TO_FIELD="//input[@id='BE_flight_arrival_city']"
    GOINGTO_RESULT_LIST="//div[@class='viewport']//div[1]/li"
    SELECT_DATE_FIELD="//input[@id='BE_flight_origin_date']"
    ALL_DATES="//div[@id='monthWrapper']//tbody//td[@class!='inActiveTD']"
    SEARCH_BUTTON="//input[@value='Search Flights']"

    def getDepartFromField(self):
        return self.waits_until_element_is_clickable(By.XPATH, self.DEPART_FROM_FIELD)

    def getGoingToField(self):

        return self.waits_until_element_is_clickable(By.XPATH, self.GOING_TO_FIELD)

    def getGoingToResults(self):
        return self.waits_presence_of_all_elements(By.XPATH, self.GOINGTO_RESULT_LIST)

    def getDepartDateField(self):
        return self.waits_until_element_is_clickable(By.XPATH, self.SELECT_DATE_FIELD)

    def getAllDatesField(self):
        return self.waits_until_element_is_clickable(By.XPATH, self.ALL_DATES)

    def getSearchButton(self):
        return self.driver.find_element(By.XPATH,self.SEARCH_BUTTON)

    def enterDepartFromLocation(self,departlocation):
        self.getDepartFromField().click()
        self.getDepartFromField().send_keys(departlocation)
        self.getDepartFromField().send_keys(Keys.ENTER)

    def enterGoingToLocation(self,goingtolocation):

        self.driver.switch_to.frame("webklipper-publisher-widget-container-notification-frame")
        self.log.info("Switched to the notification iframe")
        x_mark_locator = By.XPATH, "//*[@id='webklipper-publisher-widget-container-notification-close-div']"
        x_mark_element = self.waits_until_element_is_clickable(*x_mark_locator)
        x_mark_element.click()
        self.log.info("Clicked on the 'X' mark to close the notification")
        # Switch back to the default content
        self.driver.switch_to.default_content()
        self.getGoingToField().click()
        self.log.info("clicked on going to")
        time.sleep(2)
        self.getGoingToField().send_keys(goingtolocation)
        self.log.info("Typed text into going to field successfully")
        search_results = self.getGoingToResults()
        for results in search_results:
            if goingtolocation in results.text:
                results.click()
                break


    def enterDepartureDate(self,departuredate):
        self.getDepartDateField().click()
        all_dates=self.getAllDatesField().find_elements(By.XPATH,self.ALL_DATES)
        for date in all_dates:
            if date.get_attribute("data-date") == departuredate:
                date.click()
                break

    def clickSearchFlightsButton(self):
        self.getSearchButton().click()
        time.sleep(4)

    def searchflights(self,departlocation,goingtolocation,departuredate):
        self.enterDepartFromLocation(departlocation)
        self.enterGoingToLocation(goingtolocation)
        self.enterDepartureDate(departuredate)
        self.clickSearchFlightsButton()
        search_flights_result = SearchFlightsResults(self.driver)
        return search_flights_result
