from fdc.indices.sp500 import get_sp500_tickets
from fdc.indices.mformula import get_magic_formula_tickets, Config
from fdc.utils.browser import Browser
from fdc.yahoo.stats import get_stats
from fdc.yahoo.financials import get_financials
from fdc.indices.model import Ticket

if __name__ == '__main__':
    with Browser(debug=False) as browser:
        financials = get_financials(browser, Ticket('GILD', 'tt'))
        print(financials.to_dict())

