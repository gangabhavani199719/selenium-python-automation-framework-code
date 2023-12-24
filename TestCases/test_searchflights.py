import pytest
import softest
from Pages.yatra_launch_page import launchPage
from Utilities.utils import Utils
from ddt import ddt,data,unpack,file_data

@pytest.mark.usefixtures("setup")
@ddt
class TestSearchAndVerifyFilter(softest.TestCase):
    log = Utils.custom_logger()

    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.lp = launchPage(self.driver)
        self.ut = Utils()

    # testcase :1
    @data(("New Delhi", "New York", "25/12/2023","1 Stop"),("BOM", "New York", "27/12/2023","2 Stop"))
    @unpack
    #@file_data("../testdata/testdata.json")
    #@file_data("../testdata/testdata.yaml")
    # @data(*Utils.read_data_from_excel("C:\\python-selenium\\nsr_automation\\testdata\\excel_data.xlsx","Sheet1"))
    # @unpack
    # @data(*Utils.read_from_csv_data("C:\\python-selenium\\nsr_automation\\testdata\\csvdata.csv"))
    # @unpack
    def test_search_flights_1_stop(self,goingfrom,goingto,date,stops):
        self.log.info(f"Current URL: {self.driver.current_url}")
        search_flight_result = self.lp.searchflights(goingfrom,goingto,date)
        self.lp.page_scroll()
        search_flight_result.filter_flights_by_stop(stops)
        allstops1 = search_flight_result.get_search_flight_results()
        self.log.info(len(allstops1))
        self.ut.assertListItemText(allstops1,stops )

