from typing import Dict

import requests

from fdc.utils import proxy_list, throttle


def execute(endpoint: str, query_params: Dict[str, str]) -> requests.Response:
    throttle.throttle_for(url=endpoint)
    headers = {'User-agent': 'Mozilla/5.0'}
    proxies = proxy_list.for_requests()
    return requests.get(
        url=endpoint,
        params=query_params,
        headers=headers,
        proxies=proxies,
        timeout=(30, 30)
    )
