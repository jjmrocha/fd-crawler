import json
from typing import Dict, Optional, List

from selenium.webdriver.remote.webdriver import WebDriver

from fdc.utils import rest


class YahooBase:
    def __init__(self, data: Dict):
        self.data = data
        self._process_data_()

    def __str__(self):
        return json.dumps(self.to_dict())

    def _process_data_(self):
        raise NotImplementedError("Please implement this method")

    def to_dict(self):
        return {
            key: value.to_dict() if isinstance(value, YahooBase) else value
            for key, value in self.__dict__.items()
            if key != 'data'
        }

    def find_value(self, *field_names: str, default_value=None) -> Optional:
        value = self.data

        for name in field_names:
            value = value.get(name)
            if not value:
                return default_value

        return value


def extract_data_from_page(driver: WebDriver) -> Dict:
    _handle_consent(driver)
    app_data = driver.execute_script('return (function(root) {return root.App.main;}(this))')
    return app_data['context']['dispatcher']['stores']['QuoteSummaryStore']


def _handle_consent(driver):
    if 'consent.yahoo.com' in driver.current_url:
        driver.find_element_by_css_selector('button[type=submit]').click()


def fetch_modules(ticket: str, modules: List[str]) -> Dict:
    endpoint = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticket}'
    params = {
        'modules': ','.join(modules),
    }
    response = rest.execute(endpoint, params)
    if response.status_code != 200:
        return {}

    json_data = response.json()
    return json_data['quoteSummary']['result'][0]
