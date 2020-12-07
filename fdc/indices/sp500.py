from typing import Iterator

from fdc.model import Ticket
from fdc.utils.browser import Browser
from fdc.utils.table import parse_table, Table


def tickets(browser: Browser) -> Iterator[Ticket]:
    driver = browser.goto('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    constituents = driver.find_element_by_id('constituents')
    table = parse_table(constituents)
    return _extract_tickets(table)


def _extract_tickets(table: Table) -> Iterator[Ticket]:
    return (
        Ticket(
            code=row.get_value('Symbol'),
            name=row.get_value('Security'),
            sector=row.get_value('GICS Sector'),
            industry=row.get_value('GICS Sub-Industry'),
        )
        for row in table.rows
    )
