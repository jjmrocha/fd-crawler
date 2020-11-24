from typing import List

from fdc.yahoo.financials import (Financials, get_financials_using_api)
from fdc.yahoo.prices import (Price, get_prices_using_api)
from fdc.yahoo.stats import (Stats, get_stats_using_api)


class Ticket:
    def __init__(self, code: str, name: str = None, sector: str = None, industry: str = None):
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

    def stats(self) -> Stats:
        return get_stats_using_api(self.yahoo_code())

    def financials(self) -> Financials:
        return get_financials_using_api(self.yahoo_code())

    def prices(self) -> List[Price]:
        return get_prices_using_api(self.yahoo_code())
