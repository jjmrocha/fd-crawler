from typing import Dict

import requests

from fdc.proxy import proxy_list


def execute(endpoint: str, query_params: Dict[str, str]) -> requests.Response:
    proxies = proxy_list.for_requests()
    return requests.get(
        url=endpoint,
        params=query_params,
        proxies=proxies,
    )
