from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterator

from fdc.utils import date_util
from fdc.utils import rest


@dataclass(order=True)
class Price:
    date: datetime
    price: float


def load_using_api(ticket: str, weeks: int) -> Iterator[Price]:
    endpoint = f'https://query2.finance.yahoo.com/v8/finance/chart/{ticket}'
    end_date = date_util.now()
    start_date = end_date - timedelta(weeks=weeks)
    params = {
        'period1': date_util.to_epoch(start_date),
        'period2': date_util.to_epoch(end_date),
        'interval': '1d',
    }
    response = rest.execute(endpoint, params)
    if response.status_code != 200:
        return []

    json_data = response.json()
    dates = json_data['chart']['result'][0]['timestamp']
    values = json_data['chart']['result'][0]['indicators']['quote'][0]['close']

    return (
        Price(
            date=date_util.from_epoch(date),
            price=value,
        )
        for date, value in zip(dates, values)
    )
