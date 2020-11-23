from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from fdc.indices.model import Ticket
from fdc.utils import rest


@dataclass(order=True)
class Price:
    date: datetime
    price: float


def get_prices(ticket: Ticket) -> List[Price]:
    endpoint = f'https://query2.finance.yahoo.com/v8/finance/chart/{ticket.code}'
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=52)
    params = {
        'period1': int(start_date.timestamp()),
        'period2': int(end_date.timestamp()),
        'interval': '1d',
    }
    response = rest.execute(endpoint, params)
    if response.status_code != 200:
        return []

    json_data = response.json()
    dates = json_data['chart']['result'][0]['timestamp']
    values = json_data['chart']['result'][0]['indicators']['quote'][0]['close']

    return [
        Price(
            date=from_epoch(date),
            price=value,
        )
        for date, value in zip(dates, values)
    ]


def from_epoch(dt: int) -> datetime:
    return datetime.fromtimestamp(dt)
