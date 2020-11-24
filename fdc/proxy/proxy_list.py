from typing import List, Optional


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
_proxy_list_object = ProxyList()


def load_proxy_list(file_name: str):
    with open(file_name, 'r') as file:
        proxy_list = [
            line.strip()
            for line in file.readlines()
            if len(line.strip())
        ]

        global _proxy_list_object
        _proxy_list_object.update_list(proxy_list)


def for_requests():
    global _proxy_list_object
    next_proxy = _proxy_list_object.next_proxy()

    if next_proxy:
        return {
            'http': f'http://{next_proxy}',
            'https': f'http://{next_proxy}',
        }

    return None
