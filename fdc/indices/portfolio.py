from enum import Enum
from typing import Iterator

from fdc.model import Ticket
from fdc.utils.browser import Browser
from fdc.utils.table import parse_table, Table


class Portfolio(Enum):
    AkoCapital = 'AKO'
    FundSmith = 'FS'
    WarrenBuffet = 'BRK'
    SethKlarman = 'BAUPOST'
    ThomasGayner = 'MKL'


def tickets(browser: Browser, portfolio: Portfolio) -> Iterator[Ticket]:
    driver = browser.goto(f'https://dataroma.com/m/holdings.php?m={portfolio.value}')
    holdings = driver.find_element_by_css_selector('#main > div > table')
    table = parse_table(holdings)
    return _extract_tickets(table)


def _extract_tickets(table: Table) -> Iterator[Ticket]:
    stocks = []
    for row in table.rows:
        stock = row.get_value('Stock')
        parts = stock.split(sep='-')
        stocks.append(
            Ticket(
                code=parts[0].strip(),
                name=parts[1].strip(),
            )
        )
    return stocks
