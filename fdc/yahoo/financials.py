from typing import Optional, Dict, List

from fdc.utils.browser import Browser
from fdc.yahoo.base import extract_data_from_page, YahooBase, fetch_modules


class Financials(YahooBase):
    def _process_data_(self):
        self.balance_sheet_lq = _last_quarter_bs(
            super().find_value('balanceSheetHistoryQuarterly', default_value={})
        )
        self.balance_sheet_history = _balance_sheet_history(
            super().find_value('balanceSheetHistory', default_value={})
        )
        self.income_statement_ttm = _ttm_iss(
            super().find_value('incomeStatementHistoryQuarterly', default_value={})
        )
        self.income_statement_history = _income_statement_history(
            super().find_value('incomeStatementHistory', default_value={})
        )
        self.cash_flow_statement_ttm = _ttm_cfs(
            super().find_value('cashflowStatementHistoryQuarterly', default_value={})
        )
        self.cash_flow_statement_history = _cash_flow_statement_history(
            super().find_value('cashflowStatementHistory', default_value={})
        )

    def to_dict(self):
        return {
            key: value.to_dict() if isinstance(value, YahooBase) else (
                {
                    key: value.to_dict() if isinstance(value, YahooBase) else value
                    for key, value in value.items()
                } if isinstance(value, dict) else value
            )
            for key, value in self.__dict__.items()
            if key != 'data'
        }


class BalanceSheet(YahooBase):
    def _process_data_(self):
        self.end_date = super().find_value('endDate', 'fmt', default_value='-')
        self.total_assets = super().find_value('totalAssets', 'raw', default_value=0)
        self.current_assets = super().find_value('totalCurrentAssets', 'raw', default_value=0)
        self.cash = super().find_value('cash', 'raw', default_value=0)
        self.inventory = super().find_value('inventory', 'raw', default_value=0)
        self.property_plant_equipment = super().find_value('propertyPlantEquipment', 'raw', default_value=0)
        self.goodwill = super().find_value('goodWill', 'raw', default_value=0)
        self.total_liabilities = super().find_value('totalLiab', 'raw', default_value=0)
        self.current_liabilities = super().find_value('totalCurrentLiabilities', 'raw', default_value=0)
        self.short_term_debt = super().find_value('shortLongTermDebt', 'raw', default_value=0)
        self.long_term_debt = super().find_value('longTermDebt', 'raw', default_value=0)
        self.stockholder_equity = super().find_value('totalStockholderEquity', 'raw', default_value=0)
        self.retained_earnings = super().find_value('retainedEarnings', 'raw', default_value=0)


class IncomeStatement(YahooBase):
    def _process_data_(self):
        self.end_date = super().find_value('endDate', 'fmt', default_value='-')
        self.revenue = super().find_value('totalRevenue', 'raw', default_value=0)
        self.gross_profit = super().find_value('grossProfit', 'raw', default_value=0)
        self.sga = super().find_value('sellingGeneralAdministrative', 'raw', default_value=0)
        self.operating_income = super().find_value('operatingIncome', 'raw', default_value=0)
        self.net_income = super().find_value('netIncome', 'raw', default_value=0)
        pass


class CashFlowStatement(YahooBase):
    def _process_data_(self):
        self.end_date = super().find_value('endDate', 'fmt', default_value='-')
        self.cash_from_operating_activities = super().find_value('totalCashFromOperatingActivities', 'raw',
                                                                 default_value=0)
        self.cash_from_investing_activities = super().find_value('totalCashflowsFromInvestingActivities', 'raw',
                                                                 default_value=0)
        self.cash_from_financing_activities = super().find_value('totalCashFromFinancingActivities', 'raw',
                                                                 default_value=0)
        self.capital_expenditures = super().find_value('capitalExpenditures', 'raw', default_value=0)
        self.dividends_paid = super().find_value('dividendsPaid', 'raw', default_value=0)
        self.depreciation_and_amortization = super().find_value('depreciation', 'raw', default_value=0)


def get_financials_using_browser(browser: Browser, ticket: str):
    driver = browser.goto(f'https://finance.yahoo.com/quote/{ticket}/financials')
    data = extract_data_from_page(driver)
    return Financials(data)


def get_financials_using_api(ticket: str):
    modules = [
        'balanceSheetHistoryQuarterly',
        'balanceSheetHistory',
        'incomeStatementHistoryQuarterly',
        'incomeStatementHistory',
        'cashflowStatementHistoryQuarterly',
        'cashflowStatementHistory'
    ]
    data = fetch_modules(ticket, modules)
    return Financials(data)


def _last_quarter_bs(data: Dict) -> Optional[BalanceSheet]:
    quarters = data.get('balanceSheetStatements', [])
    if len(quarters) == 0:
        return None
    return BalanceSheet(quarters[0])


def _balance_sheet_history(data: Dict) -> Dict[str, BalanceSheet]:
    return {
        _safe_end_date(year_dict): BalanceSheet(year_dict)
        for year_dict in data.get('balanceSheetStatements', [])
    }


def _ttm_iss(data: Dict) -> Optional[IncomeStatement]:
    quarters = data.get('incomeStatementHistory', [])
    if len(quarters) < 4:
        return None
    ttm = _compute_ttm(quarters[0:4])
    return IncomeStatement(ttm)


def _income_statement_history(data: Dict) -> Dict[str, IncomeStatement]:
    return {
        _safe_end_date(year_dict): IncomeStatement(year_dict)
        for year_dict in data.get('incomeStatementHistory', [])
    }


def _ttm_cfs(data: Dict) -> Optional[CashFlowStatement]:
    quarters = data.get('cashflowStatements', [])
    if len(quarters) < 4:
        return None
    ttm = _compute_ttm(quarters[0:4])
    return CashFlowStatement(ttm)


def _cash_flow_statement_history(data: Dict) -> Dict[str, CashFlowStatement]:
    return {
        _safe_end_date(year_dict): CashFlowStatement(year_dict)
        for year_dict in data.get('cashflowStatements', [])
    }


def _delete_unused_fields(entries: Dict) -> Dict:
    new_dict = {}

    for key, value in entries.items():
        if not isinstance(value, dict):
            continue

        if key == 'endDate':
            new_dict[key] = {'fmt': value.get('fmt', '-')}
        else:
            new_dict[key] = {'raw': value.get('raw', 0)}

    return new_dict


def _compute_ttm(quarters: List[Dict]) -> Dict:
    last = _delete_unused_fields(quarters[0])

    for quarter in quarters[1:]:
        for key, value in quarter.items():
            if key == 'endDate':
                continue
            if not isinstance(value, dict):
                continue

            old_value = last.get(key, {}).get('raw', 0)
            value_to_add = value.get('raw', 0)
            last[key] = {'raw': old_value + value_to_add}

    return last


def _safe_end_date(year_dict):
    return year_dict.get('endDate', {}).get('fmt', '-')
