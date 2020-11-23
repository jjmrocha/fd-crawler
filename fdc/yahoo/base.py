from typing import Dict, Optional

from selenium.webdriver.remote.webdriver import WebDriver


class YahooBase:
    def __init__(self, data: Dict):
        self.data = data
        self._process_data_()

    def _process_data_(self):
        raise NotImplementedError("Please Implement this method")

    def find_value(self, *field_names: str) -> Optional:
        value = self.data

        for name in field_names:
            value = value.get(name)
            if not value:
                return None

        return value


def extract_data_from_page(driver: WebDriver) -> Dict:
    _handle_consent(driver)
    app_data = driver.execute_script('return (function(root) {return root.App.main;}(this))')
    return app_data['context']['dispatcher']['stores']['QuoteSummaryStore']


def _handle_consent(driver):
    if 'consent.yahoo.com' in driver.current_url:
        driver.find_element_by_css_selector('button[type=submit]').click()
