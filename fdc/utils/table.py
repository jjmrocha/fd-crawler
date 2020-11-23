from typing import Optional, Dict, Iterable, List
from selenium.webdriver.remote.webelement import WebElement


class Row:
    def __init__(self, row_data: Dict[str, str] = None):
        self.data = row_data if row_data else {}

    def get_columns(self) -> Iterable[str]:
        return self.data.keys()

    def add_value(self, column: str, value: str):
        self.data[column] = value

    def get_value(self, column: str, default: str = None) -> Optional[str]:
        return self.data.get(column, default)

    @classmethod
    def from_values(cls, columns: List[str], values: List[str]):
        row_data = dict(zip(columns, values))
        return cls(row_data)


class Table:
    def __init__(self, columns: List[str] = None):
        self.columns = columns if columns else []
        self.rows = []

    def add_row(self, row: Row):
        self.rows.append(row)

    def get_column(self, column: str) -> List[str]:
        return [
            row.get_value(column)
            for row in self.rows
        ]


def _extract_columns(table_element: WebElement) -> List[str]:
    first_row = table_element.find_element_by_tag_name('tr')
    columns = []

    th_elements = first_row.find_elements_by_tag_name('th')
    for element in th_elements:
        columns.append(element.text)

    if columns:
        return columns

    td_elements = first_row.find_elements_by_tag_name('td')
    for element in td_elements:
        columns.append(element.text)

    return columns


def _extract_row_elements(table_element: WebElement) -> List[WebElement]:
    row_elements = table_element.find_elements_by_tag_name('tr')
    return row_elements[1:]


def _extract_values(row_element: WebElement) -> List[str]:
    return [
        element.text
        for element in row_element.find_elements_by_tag_name('td')
    ]


def parse_table(table_element: WebElement) -> Table:
    columns = _extract_columns(table_element)

    table = Table(columns)

    row_elements = _extract_row_elements(table_element)
    for row_element in row_elements:
        values = _extract_values(row_element)
        row = Row.from_values(columns, values)
        table.add_row(row)

    return table
