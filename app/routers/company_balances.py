import yfinance as yf
from typing import Dict, Any, List, Optional


def fetch_balance_sheet(ticker: str) -> Dict[str, Any]:
    """
    Fetch balance sheet data for the given ticker using yfinance.

    :param ticker: Stock ticker symbol
    :return: A dictionary containing balance sheet data similar to Alpha Vantage
    """
    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)

        # Get balance sheet data (most recent annual reports)
        balance_sheet = stock.balance_sheet
        if balance_sheet.empty:
            return {"symbol": ticker, "annualReports": []}

        # Parse balance sheet data to match the desired structure
        annual_reports: List[Dict[str, Optional[Any]]] = []
        for fiscal_date, values in balance_sheet.items():
            annual_report = {
                "fiscalDateEnding": fiscal_date.strftime("%Y-%m-%d") if fiscal_date else None,
                "reportedCurrency": stock.info.get("currency", None),
                "totalAssets": values.get("Total Assets", None),
                "totalCurrentAssets": values.get("Total Current Assets", None),
                "cashAndCashEquivalentsAtCarryingValue": values.get("Cash And Cash Equivalents", None),
                "cashAndShortTermInvestments": values.get("Cash And Short Term Investments", None),
                "inventory": values.get("Inventory", None),
                "currentNetReceivables": values.get("Net Receivables", None),
                "totalNonCurrentAssets": values.get("Total Non Current Assets", None),
                "propertyPlantEquipment": values.get("Property Plant And Equipment", None),
                "accumulatedDepreciationAmortizationPPE": values.get("Accumulated Depreciation", None),
                "intangibleAssets": values.get("Intangible Assets", None),
                "intangibleAssetsExcludingGoodwill": values.get("Intangible Assets Excluding Goodwill", None),
                "goodwill": values.get("Goodwill", None),
                "investments": values.get("Investments", None),
                "longTermInvestments": values.get("Long Term Investments", None),
                "shortTermInvestments": values.get("Short Term Investments", None),
                "otherCurrentAssets": values.get("Other Current Assets", None),
                "otherNonCurrentAssets": values.get("Other Non Current Assets", None),
                "totalLiabilities": values.get("Total Liabilities", None),
                "totalCurrentLiabilities": values.get("Total Current Liabilities", None),
                "currentAccountsPayable": values.get("Accounts Payable", None),
                "deferredRevenue": values.get("Deferred Revenue", None),
                "currentDebt": values.get("Current Debt", None),
                "shortTermDebt": values.get("Short Term Debt", None),
                "totalNonCurrentLiabilities": values.get("Total Non Current Liabilities", None),
                "capitalLeaseObligations": values.get("Capital Lease Obligations", None),
                "longTermDebt": values.get("Long Term Debt", None),
                "currentLongTermDebt": values.get("Current Long Term Debt", None),
                "longTermDebtNoncurrent": values.get("Long Term Debt Non Current", None),
                "shortLongTermDebtTotal": values.get("Short Long Term Debt Total", None),
                "otherCurrentLiabilities": values.get("Other Current Liabilities", None),
                "otherNonCurrentLiabilities": values.get("Other Non Current Liabilities", None),
                "totalShareholderEquity": values.get("Total Shareholder Equity", None),
                "treasuryStock": values.get("Treasury Stock", None),
                "retainedEarnings": values.get("Retained Earnings", None),
                "commonStock": values.get("Common Stock", None),
                "commonStockSharesOutstanding": stock.info.get("sharesOutstanding", None),
            }
            annual_reports.append(annual_report)

        return {"symbol": ticker, "annualReports": annual_reports}

    except Exception as e:
        raise ValueError(f"Error fetching balance sheet data for ticker {ticker}: {str(e)}")
