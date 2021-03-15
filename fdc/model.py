from typing import Iterator

from fdc.utils.browser import Browser
from fdc.yahoo import (financials, prices, stats)


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

    def __eq__(self, other):
        return (
            self.code == other.code
            if isinstance(other, Ticket)
            else False
        )

    def yahoo_code(self):
        return self.code.replace('.', '-')

    def use_browser_when_possible(self, browser: Browser):
        self.browser = browser

    def stats(self) -> stats.Stats:
        return (
            stats.load_using_browser(self.browser, self.yahoo_code()) if self.browser
            else stats.load_using_api(self.yahoo_code())
        )

    def financials(self) -> financials.Financials:
        return (
            financials.load_using_browser(self.browser, self.yahoo_code()) if self.browser
            else financials.load_using_api(self.yahoo_code())
        )

    def prices(self, weeks: int = 52) -> Iterator[prices.Price]:
        return prices.load_using_api(self.yahoo_code(), weeks)
