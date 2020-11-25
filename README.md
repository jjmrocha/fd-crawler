fd-crawler
==========
Finance crawler for reading financial data from public sites


Requirements
------------
1. python3
2. pipenv
3. chromedriver

Setup
-----
1. Initialize pipenv virtual env
    ```
    pipenv --python 3.7
    ``` 

2. Install dependencies
   ```
   pipenv install --dev
   ```
   
3. Install Chrome Driver
   * Download from `http://chromedriver.chromium.org/`
   * Add `chromedriver` to your `PATH`
   

How-to import
-------------
```
pipenv install git+https://github.com/jjmrocha/fd-crawler.git#egg=fd-crawler
```

   
How-to Use
----------
The following program:
```python
import time

from fdc.indices.sp500 import get_sp500_tickets
from fdc.utils import date_util
from fdc.utils.browser import Browser

if __name__ == '__main__':
    with Browser() as browser:
        for ticket in get_sp500_tickets(browser):
            print(f'- {ticket.code} - {ticket.name} ({ticket.sector})')
            # Stats
            stats = ticket.stats()
            print(f'   > market_cap: {stats.market_cap} ebitda: {stats.ebitda}')
            # Financials
            financials = ticket.financials()
            print(f'   > lq_stockholder_equity: {financials.balance_sheet_lq.stockholder_equity} '
                  f'ttm_revenue: {financials.income_statement_ttm.revenue} '
                  f'ttm_dividends_paid: {financials.cash_flow_statement_ttm.dividends_paid}')
            # Prices
            prices = ticket.prices()
            if len(prices):
                price_52w = prices[0]
                price_last = prices[-1]
                print(f'   > {date_util.to_iso8601_date(price_52w.date)}: {price_52w.price} '
                      f'- {date_util.to_iso8601_date(price_last.date)}: {price_last.price}')
            print()
            # Sleep for 3 seconds to not upset Yahoo
            time.sleep(3)
```

Will produce:
```
- MMM - 3M Company (Industrials)
   > market_cap: 100447789056 ebitda: 8686999552
   > lq_stockholder_equity: 11880000000 ttm_revenue: 31712000000 ttm_dividends_paid: -3368000000
   > 2019-11-26: 169.22999572753906 - 2020-11-23: 174.13999938964844

- ABT - Abbott Laboratories (Health Care)
   > market_cap: 193665761280 ebitda: 7823000064
   > lq_stockholder_equity: 31386000000 ttm_revenue: 32221000000 ttm_dividends_paid: -2487000000
   > 2019-11-26: 85.41999816894531 - 2020-11-23: 109.2699966430664

- ABBV - AbbVie Inc. (Health Care)
   > market_cap: 180330332160 ebitda: 18371999744
   > lq_stockholder_equity: 15270000000 ttm_revenue: 40650000000 ttm_dividends_paid: -7210000000
   > 2019-11-26: 87.72000122070312 - 2020-11-23: 102.18000030517578
...
```
   
License
-------
Any contributions made under this project will be governed by the [MIT License](./LICENSE.md).