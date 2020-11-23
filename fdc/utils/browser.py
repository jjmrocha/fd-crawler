from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


class Browser:
    def __init__(self, debug: bool = False, timeout: int = 5):
        options = _create_options(debug)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(timeout)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def goto(self, url: str) -> WebDriver:
        self.driver.get(url)
        return self.driver

    def cookie(self, name: str, value: str):
        self.driver.add_cookie({'name': name, 'value': value})

    def close(self):
        self.driver.quit()


def _create_options(debug: bool) -> Options:
    options = Options()
    options.add_argument('--window-size=1400,1050')
    options.add_argument('--lang=en')

    if debug:
        options.add_argument('--verbose')
    else:
        options.add_argument("--headless")

    return options
