from fdc.indices.model import Ticket
from fdc.utils.browser import Browser
from fdc.yahoo.base import extract_data_from_page, YahooBase


class Stats(YahooBase):
    def _process_data_(self):
        self.price = super().find_value('financialData', 'currentPrice', 'raw')
        self.market_cap = super().find_value('price', 'marketCap', 'raw')
        self.enterprise_value = super().find_value('defaultKeyStatistics', 'enterpriseValue', 'raw')
        self.ebitda = super().find_value('financialData', 'ebitda', 'raw')
        self.levered_fcf = super().find_value('financialData', 'freeCashflow', 'raw')
        self.dividend = super().find_value('summaryDetail', 'dividendRate', 'raw')
        self.dividend_yield = super().find_value('summaryDetail', 'dividendYield', 'raw')
        self.book_value = super().find_value('defaultKeyStatistics', 'bookValue', 'raw')


def get_stats(browser: Browser, ticket: Ticket):
    driver = browser.goto(f'https://finance.yahoo.com/quote/{ticket.code}/key-statistics')
    data = extract_data_from_page(driver)
    return Stats(data)
