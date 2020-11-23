class Ticket:
    def __init__(self, code: str, name: str, sector: str = None, industry: str = None):
        self.code = code
        self.name = name
        self.sector = sector
        self.industry = industry

    def __str__(self):
        return f'{self.code} - {self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.code}, {self.name})'
