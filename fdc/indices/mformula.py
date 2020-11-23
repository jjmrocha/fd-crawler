import json
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver

from fdc.indices.model import Ticket
from fdc.utils.browser import Browser
from fdc.utils.table import parse_table, Table


class Config(object):
    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            json_data = json.load(file)

        self.username = json_data['username']
        self.password = json_data['password']


def get_magic_formula_tickets(browser: Browser,
                              config: Config,
                              threshold: int = 50,
                              top50: bool = True) -> List[Ticket]:
    driver = browser.goto('https://www.magicformulainvesting.com/Account/LogOn')
    _do_login(driver, config)
    _do_query(driver, threshold, top50)
    constituents = driver.find_element_by_css_selector('#tableform > table')
    table = parse_table(constituents)
    return _extract_tickets(table)


def _do_login(driver: WebDriver, config: Config):
    driver.find_element_by_id('Email').send_keys(config.username)
    driver.find_element_by_id('Password').send_keys(config.password)
    driver.find_element_by_id('login').click()


def _do_query(driver: WebDriver, threshold: int, top50: bool):
    mmc_element = driver.find_element_by_id('MinimumMarketCap')
    mmc_element.clear()
    mmc_element.send_keys(threshold)

    if top50:
        driver.find_element_by_css_selector('input[value=false]').click()
    else:
        driver.find_element_by_css_selector('input[value=true]').click()

    driver.find_element_by_id('stocks').click()


def _extract_tickets(table: Table) -> List[Ticket]:
    return [
        Ticket(
            code=row.get_value('Ticker'),
            name=row.get_value('Company Name (in alphabetical order)'),
        )
        for row in table.rows
    ]
