import time
from datetime import timedelta
from urllib import parse

from fdc.utils import date_util


class Throttle:
    def __init__(self):
        self.min_delay = timedelta(milliseconds=0)
        self.hosts = {}

    def set_min_delay(self, value_in_millis: int):
        self.min_delay = timedelta(milliseconds=value_in_millis)

    def throttle(self, url: str):
        host = parse.urlsplit(url).hostname
        next_request_date = self.hosts.get(host, date_util.min_datetime)
        now = date_util.now()

        if now < next_request_date:
            waiting_time = next_request_date - now
            time.sleep(waiting_time.total_seconds())

        self.hosts[host] = date_util.now() + self.min_delay


# Global var
_throttle_object_ = Throttle()


def set_throttle(delay_in_millis: int):
    global _throttle_object_
    _throttle_object_.set_min_delay(delay_in_millis)


def throttle_for(url: str):
    global _throttle_object_
    _throttle_object_.throttle(url)
