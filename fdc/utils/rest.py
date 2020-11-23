from typing import Dict

import requests


def execute(endpoint: str, query_params: Dict[str, str]) -> requests.Response:
    return requests.get(
        url=endpoint,
        params=query_params,
    )
