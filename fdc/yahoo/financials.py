from typing import Optional, Dict, List

from fdc.indices.model import Ticket
from fdc.utils.browser import Browser
from fdc.yahoo.base import extract_data_from_page, YahooBase


class Financials(YahooBase):
    def _process_data_(self):
        self.balance_sheet_lq = _last_quarter_bs(self.data.get('balanceSheetHistoryQuarterly', {}))
        self.balance_sheet_history = _balance_sheet_history(self.data.get('balanceSheetHistory', {}))
        self.income_statement_ttm = _ttm_iss(self.data.get('incomeStatementHistoryQuarterly', {}))
        self.income_statement_history = _income_statement_history(self.data.get('incomeStatementHistory', {}))
        self.cash_flow_statement_ttm = _ttm_cfs(self.data.get('cashflowStatementHistoryQuarterly', {}))
        self.cash_flow_statement_history = _cash_flow_statement_history(self.data.get('cashflowStatementHistory', {}))


class BalanceSheet(YahooBase):
    def _process_data_(self):
        self.end_date = super().find_value('endDate', 'fmt')
        self.total_assets = super().find_value('totalAssets', 'raw')
        self.current_assets = super().find_value('totalCurrentAssets', 'raw')
        self.cash = super().find_value('cash', 'raw')
        self.inventory = super().find_value('inventory', 'raw')
        self.property_plant_equipment = super().find_value('propertyPlantEquipment', 'raw')
        self.goodwill = super().find_value('goodWill', 'raw')
        self.total_liabilities = super().find_value('totalLiab', 'raw')
        self.current_liabilities = super().find_value('totalCurrentLiabilities', 'raw')
        self.short_term_debt = super().find_value('shortLongTermDebt', 'raw')
        self.long_term_debt = super().find_value('longTermDebt', 'raw')
        self.stockholder_equity = super().find_value('totalStockholderEquity', 'raw')
        self.retained_earnings = super().find_value('retainedEarnings', 'raw')

    def invested_capital(self):
        return self.total_assets - self.current_liabilities - self.cash


class IncomeStatement(YahooBase):
    def _process_data_(self):
        self.end_date = super().find_value('endDate', 'fmt')
        self.revenue = super().find_value('totalRevenue', 'raw')
        self.gross_profit = super().find_value('grossProfit', 'raw')
        self.sga = super().find_value('sellingGeneralAdministrative', 'raw')
        self.operating_income = super().find_value('operatingIncome', 'raw')
        self.net_income = super().find_value('netIncome', 'raw')
        pass


class CashFlowStatement(YahooBase):
    def _process_data_(self):
        self.end_date = super().find_value('endDate', 'fmt')
        self.cash_from_operating_activities = super().find_value('totalCashFromOperatingActivities', 'raw')
        self.cash_from_investing_activities = super().find_value('totalCashflowsFromInvestingActivities', 'raw')
        self.cash_from_financing_activities = super().find_value('totalCashFromFinancingActivities', 'raw')
        self.capital_expenditures = super().find_value('capitalExpenditures', 'raw')
        self.dividends_paid = super().find_value('dividendsPaid', 'raw')
        self.depreciation_and_amortization = super().find_value('depreciation', 'raw')


def get_financials(browser: Browser, ticket: Ticket):
    driver = browser.goto(f'https://finance.yahoo.com/quote/{ticket.code}/financials')
    data = extract_data_from_page(driver)
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
        if key == 'endDate':
            new_dict[key] = {'fmt': value.get('fmt', '-')}
        else:
            new_dict[key] = {'raw': value.get('raw', 0)}

    return new_dict


def _compute_ttm(quarters: List[Dict]) -> Dict:
    last = _delete_unused_fields(quarters[0])

    for quarter in quarters[1:]:
        for key, value in quarter.items():
            if key != 'endDate':
                old_value = last.get(key, 0)
                value_to_add = value.get('raw', 0)
                last[key] = {'raw': old_value + value_to_add}

    return last


def _safe_end_date(year_dict):
    return year_dict.get('endDate', {}).get('fmt', '-')
