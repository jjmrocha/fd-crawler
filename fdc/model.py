from typing import List

from fdc.yahoo.financials import (Financials, get_financials_using_api, get_financials_using_browser)
from fdc.yahoo.prices import (Price, get_prices_using_api)
from fdc.yahoo.stats import (Stats, get_stats_using_api, get_stats_using_browser)
from fdc.utils.browser import Browser


class Ticket:
    def __init__(self, code: str, name: str = None, sector: str = None, industry: str = None):
        self.browser = None
        self.code = code
        self.name = name
        self.sector = sector
        self.industry = industry

    def __str__(self):
        return f'{self.code} - {self.name}' if self.name else self.code

    def __repr__(self):
        return f'{self.__class__.__name__}({self.code}, {self.name})'

    def yahoo_code(self):
        return self.code.replace('.', '-')

    def use_browser_when_possible(self, browser: Browser):
        self.browser = browser

    def stats(self) -> Stats:
        return (
            get_stats_using_browser(self.browser, self.yahoo_code()) if self.browser
            else get_stats_using_api(self.yahoo_code())
        )

    def financials(self) -> Financials:
        return (
            get_financials_using_browser(self.browser, self.yahoo_code()) if self.browser
            else get_financials_using_api(self.yahoo_code())
        )

    def prices(self) -> List[Price]:
        return get_prices_using_api(self.yahoo_code())
