from fdc.utils.browser import Browser
from fdc.yahoo.base import extract_data_from_page, YahooBase, fetch_modules


class Stats(YahooBase):
    def _process_data_(self):
        self.price = super().find_value('financialData', 'currentPrice', 'raw', default_value=0)
        self.market_cap = super().find_value('price', 'marketCap', 'raw', default_value=0)
        self.enterprise_value = super().find_value('defaultKeyStatistics', 'enterpriseValue', 'raw', default_value=0)
        self.ebitda = super().find_value('financialData', 'ebitda', 'raw', default_value=0)
        self.levered_fcf = super().find_value('financialData', 'freeCashflow', 'raw', default_value=0)
        self.dividend = super().find_value('summaryDetail', 'dividendRate', 'raw', default_value=0)
        self.dividend_yield = super().find_value('summaryDetail', 'dividendYield', 'raw', default_value=0)
        self.book_value = super().find_value('defaultKeyStatistics', 'bookValue', 'raw', default_value=0)


def get_stats_using_browser(browser: Browser, ticket: str):
    driver = browser.goto(f'https://finance.yahoo.com/quote/{ticket}/key-statistics')
    data = extract_data_from_page(driver)
    return Stats(data)


def get_stats_using_api(ticket: str):
    modules = ['financialData', 'price', 'defaultKeyStatistics', 'summaryDetail']
    data = fetch_modules(ticket, modules)
    return Stats(data)
