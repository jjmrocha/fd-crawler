from fdc.model import Ticket
from fdc.utils.browser import Browser
from fdc.yahoo import financials
from fdc.yahoo import prices
from fdc.yahoo import stats

if __name__ == '__main__':
    stock = Ticket('GILD')

    with Browser(debug=False) as browser:
        stats = stats.get_stats(browser, stock)
        print('stats', stats)
        financials = financials.get_financials(browser, stock)
        print('financials', financials)
        prices = prices.get_prices(stock)
        print('prices', str(prices))
