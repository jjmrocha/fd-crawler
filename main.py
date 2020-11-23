from fdc.indices.model import Ticket
from fdc.utils.browser import Browser
from fdc.yahoo.financials import get_financials
from fdc.yahoo.stats import get_stats

if __name__ == '__main__':
    stock = Ticket('GILD')

    with Browser(debug=False) as browser:
        stats = get_stats(browser, stock)
        print('stats', stats)
        financials = get_financials(browser, stock)
        print('financials', financials)
