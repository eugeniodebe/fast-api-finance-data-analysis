from sqlalchemy import Column, Enum, Integer, String, Float, ForeignKey, Date, BigInteger, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class StockSymbolORM(Base):
    __tablename__ = "stock_symbols"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    exchange = Column(String)
    currency = Column(String)
    sector = Column(String)
    industry = Column(String)

    # Establish relationship with StockOverviewORM
    stock_overview = relationship("StockOverviewORM", back_populates="stock_symbol", uselist=False)
    financial_balances = relationship("FinancialBalanceORM", back_populates="stock_symbol", cascade="all, delete-orphan")

class StockOverviewORM(Base):
    __tablename__ = "stock_overview"

    id = Column(Integer, primary_key=True, index=True)
    stock_symbol_id = Column(Integer, ForeignKey("stock_symbols.id"), nullable=False)
    market_capitalization = Column(Float)
    book_value = Column(Float)
    trailing_pe = Column(Float)
    forward_pe = Column(Float)
    dividend_per_share = Column(Float)
    dividend_yield = Column(Float)
    eps = Column(Float)
    revenue_ttm = Column(Float)
    profit_margin = Column(Float)
    beta = Column(Float)
    fifty_two_week_high = Column(Float)
    fifty_two_week_low = Column(Float)
    shares_outstanding = Column(Float)

    # Establish relationship with StockSymbolORM
    stock_symbol = relationship("StockSymbolORM", back_populates="stock_overview")

class FinancialBalanceORM(Base):
    __tablename__ = "financial_balances"
    id = Column(Integer, primary_key=True, index=True)
    stock_symbol_id = Column(Integer, ForeignKey("stock_symbols.id", ondelete="CASCADE"), nullable=False)
    # fiscal_date = Column(String, nullable=False)  # Store the fiscal date as text for simplicity
    fiscal_date = Column(Date, nullable=False)  # Change to Date type
    feature_type = Column(String, nullable=False)  # New field
    treasury_shares_number = Column(Float, nullable=True)
    ordinary_shares_number = Column(Float, nullable=True)
    share_issued = Column(Float, nullable=True)
    net_debt = Column(Float, nullable=True)
    total_debt = Column(Float, nullable=True)
    tangible_book_value = Column(Float, nullable=True)
    invested_capital = Column(Float, nullable=True)
    working_capital = Column(Float, nullable=True)
    net_tangible_assets = Column(Float, nullable=True)
    capital_lease_obligations = Column(Float, nullable=True)
    common_stock_equity = Column(Float, nullable=True)
    total_capitalization = Column(Float, nullable=True)
    total_equity_gross_minority_interest = Column(Float, nullable=True)
    stockholders_equity = Column(Float, nullable=True)
    gains_losses_not_affecting_retained_earnings = Column(Float, nullable=True)
    other_equity_adjustments = Column(Float, nullable=True)
    retained_earnings = Column(Float, nullable=True)
    capital_stock = Column(Float, nullable=True)
    common_stock = Column(Float, nullable=True)
    total_liabilities_net_minority_interest = Column(Float, nullable=True)
    total_non_current_liabilities_net_minority_interest = Column(Float, nullable=True)
    other_non_current_liabilities = Column(Float, nullable=True)
    trade_and_other_payables_non_current = Column(Float, nullable=True)
    long_term_debt_and_capital_lease_obligation = Column(Float, nullable=True)
    long_term_capital_lease_obligation = Column(Float, nullable=True)
    long_term_debt = Column(Float, nullable=True)
    current_liabilities = Column(Float, nullable=True)
    other_current_liabilities = Column(Float, nullable=True)
    current_deferred_liabilities = Column(Float, nullable=True)
    current_deferred_revenue = Column(Float, nullable=True)
    current_debt_and_capital_lease_obligation = Column(Float, nullable=True)
    current_capital_lease_obligation = Column(Float, nullable=True)
    current_debt = Column(Float, nullable=True)
    other_current_borrowings = Column(Float, nullable=True)
    commercial_paper = Column(Float, nullable=True)
    payables_and_accrued_expenses = Column(Float, nullable=True)
    payables = Column(Float, nullable=True)
    total_tax_payable = Column(Float, nullable=True)
    income_tax_payable = Column(Float, nullable=True)
    accounts_payable = Column(Float, nullable=True)
    total_assets = Column(Float, nullable=True)
    total_non_current_assets = Column(Float, nullable=True)
    other_non_current_assets = Column(Float, nullable=True)
    non_current_deferred_assets = Column(Float, nullable=True)
    non_current_deferred_taxes_assets = Column(Float, nullable=True)
    investments_and_advances = Column(Float, nullable=True)
    other_investments = Column(Float, nullable=True)
    investment_in_financial_assets = Column(Float, nullable=True)
    available_for_sale_securities = Column(Float, nullable=True)
    net_ppe = Column(Float, nullable=True)
    accumulated_depreciation = Column(Float, nullable=True)
    gross_ppe = Column(Float, nullable=True)
    leases = Column(Float, nullable=True)
    other_properties = Column(Float, nullable=True)
    machinery_furniture_equipment = Column(Float, nullable=True)
    land_and_improvements = Column(Float, nullable=True)
    properties = Column(Float, nullable=True)
    current_assets = Column(Float, nullable=True)
    other_current_assets = Column(Float, nullable=True)
    inventory = Column(Float, nullable=True)
    receivables = Column(Float, nullable=True)
    other_receivables = Column(Float, nullable=True)
    accounts_receivable = Column(Float, nullable=True)
    cash_cash_equivalents_and_short_term_investments = Column(Float, nullable=True)
    other_short_term_investments = Column(Float, nullable=True)
    cash_and_cash_equivalents = Column(Float, nullable=True)
    cash_equivalents = Column(Float, nullable=True)
    cash_financial = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Relationship with StockSymbolORM
    stock_symbol = relationship("StockSymbolORM", back_populates="financial_balances")