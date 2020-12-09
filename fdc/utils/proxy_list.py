from typing import List, Optional, Dict


class ProxyList:
    def __init__(self):
        self.proxy_list = []
        self.current = 0

    def next_proxy(self) -> Optional[str]:
        if len(self.proxy_list) == 0:
            return None

        index = self.current
        next_proxy = self.proxy_list[index]

        if index + 1 >= len(self.proxy_list):
            self.current = 0
        else:
            self.current = index + 1

        return next_proxy

    def update_list(self, proxy_list: List[str]):
        self.proxy_list = proxy_list


# Global var
_proxy_list_object_ = ProxyList()


def load_proxy_list(file_name: str):
    with open(file_name, 'r') as file:
        proxy_list = [
            line.strip()
            for line in file.readlines()
            if len(line.strip())
        ]

        global _proxy_list_object_
        _proxy_list_object_.update_list(proxy_list)


def add_proxy(host: str, port: int):
    global _proxy_list_object_
    _proxy_list_object_.proxy_list.append(f'{host}:{port}')


def for_requests() -> Optional[Dict[str, str]]:
    global _proxy_list_object_
    next_proxy = _proxy_list_object_.next_proxy()

    if next_proxy is not None:
        return {
            'http': f'http://{next_proxy}',
            'https': f'http://{next_proxy}',
        }

    return None


def for_browser() -> Optional[str]:
    global _proxy_list_object_
    return _proxy_list_object_.next_proxy()
