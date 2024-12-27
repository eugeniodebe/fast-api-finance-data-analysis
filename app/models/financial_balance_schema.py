from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Enum



class FinancialBalanceSchema(BaseModel):
    id: Optional[int] = None
    fiscal_date: str
    # feature_type: str  # Change from Enum to str
    fiscal_date: date  # Change to date type
    stock_symbol_id: int
    treasury_shares_number: Optional[float] = None
    ordinary_shares_number: Optional[float] = None
    share_issued: Optional[float] = None
    net_debt: Optional[float] = None
    total_debt: Optional[float] = None
    tangible_book_value: Optional[float] = None
    invested_capital: Optional[float] = None
    working_capital: Optional[float] = None
    net_tangible_assets: Optional[float] = None
    capital_lease_obligations: Optional[float] = None
    common_stock_equity: Optional[float] = None
    total_capitalization: Optional[float] = None
    total_equity_gross_minority_interest: Optional[float] = None
    stockholders_equity: Optional[float] = None
    gains_losses_not_affecting_retained_earnings: Optional[float] = None
    other_equity_adjustments: Optional[float] = None
    retained_earnings: Optional[float] = None
    capital_stock: Optional[float] = None
    common_stock: Optional[float] = None
    total_liabilities_net_minority_interest: Optional[float] = None
    total_non_current_liabilities_net_minority_interest: Optional[float] = None
    other_non_current_liabilities: Optional[float] = None
    trade_and_other_payables_non_current: Optional[float] = None
    long_term_debt_and_capital_lease_obligation: Optional[float] = None
    long_term_capital_lease_obligation: Optional[float] = None
    long_term_debt: Optional[float] = None
    current_liabilities: Optional[float] = None
    other_current_liabilities: Optional[float] = None
    current_deferred_liabilities: Optional[float] = None
    current_deferred_revenue: Optional[float] = None
    current_debt_and_capital_lease_obligation: Optional[float] = None
    current_capital_lease_obligation: Optional[float] = None
    current_debt: Optional[float] = None
    other_current_borrowings: Optional[float] = None
    commercial_paper: Optional[float] = None
    payables_and_accrued_expenses: Optional[float] = None
    payables: Optional[float] = None
    total_tax_payable: Optional[float] = None
    income_tax_payable: Optional[float] = None
    accounts_payable: Optional[float] = None
    total_assets: Optional[float] = None
    total_non_current_assets: Optional[float] = None
    other_non_current_assets: Optional[float] = None
    non_current_deferred_assets: Optional[float] = None
    non_current_deferred_taxes_assets: Optional[float] = None
    investments_and_advances: Optional[float] = None
    other_investments: Optional[float] = None
    investment_in_financial_assets: Optional[float] = None
    available_for_sale_securities: Optional[float] = None
    net_ppe: Optional[float] = None
    accumulated_depreciation: Optional[float] = None
    gross_ppe: Optional[float] = None
    leases: Optional[float] = None
    other_properties: Optional[float] = None
    machinery_furniture_equipment: Optional[float] = None
    land_and_improvements: Optional[float] = None
    properties: Optional[float] = None
    current_assets: Optional[float] = None
    other_current_assets: Optional[float] = None
    inventory: Optional[float] = None
    receivables: Optional[float] = None
    other_receivables: Optional[float] = None
    accounts_receivable: Optional[float] = None
    cash_cash_equivalents_and_short_term_investments: Optional[float] = None
    other_short_term_investments: Optional[float] = None
    cash_and_cash_equivalents: Optional[float] = None
    cash_equivalents: Optional[float] = None
    cash_financial: Optional[float] = None

   


    class Config:
        orm_mode = True