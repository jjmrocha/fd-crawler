from datetime import datetime

import pytz
from dateutil import parser


def to_iso8601(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def to_iso8601_date(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d')


def to_epoch(dt: datetime) -> int:
    return int(dt.timestamp())


def from_iso8601(dt: str) -> datetime:
    return parser.parse(dt)


def from_epoch(dt: int) -> datetime:
    return datetime.fromtimestamp(dt, tz=pytz.UTC)


def now() -> datetime:
    return datetime.now(tz=pytz.UTC)
