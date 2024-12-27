from datetime import datetime
from typing import Any, List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security.verify_secret import verify_secret
from app.database.connection import get_db
from app.database.models.finance.stock_models import FinancialBalanceORM, StockSymbolORM, StockOverviewORM
from app.helpers.helper_names import  convert_keys_to_snake_case, filter_valid_columns, replace_nan_with_none
# from app.models.financial_balance_schema import FinancialBalanceSchema
from app.models.financial_balance_schema import FinancialBalanceSchema
from app.models.stock_overview_schema import StockOverviewSchema
from sqlalchemy.orm import joinedload
import yfinance as yf
import numpy as np
from dateutil.parser import parse




router = APIRouter()

# @router.get("/stock/overview/{ticker}", response_model=StockOverviewSchema)
# def get_stock_overview(ticker: str, session: AsyncSession = Depends(get_db), x_secret_key: str = Depends(verify_secret)):
#     try:
#         # Fetch stock data using yfinance

#         stock = yf.Ticker(ticker)
#         info = stock.info

#         # Map the available data to the StockOverviewORM model
#         overview = StockOverviewORM(
#             symbol=info.get("symbol", ticker),
#             name=info.get("shortName"),
#             description=info.get("longBusinessSummary"),
#             exchange=info.get("exchange"),
#             currency=info.get("currency"),
#             country=info.get("country"),
#             sector=info.get("sector"),
#             industry=info.get("industry"),
#             market_capitalization=info.get("marketCap"),
#             book_value=info.get("bookValue"),
#             trailing_pe=info.get("trailingPE"),
#             forward_pe=info.get("forwardPE"),
#             dividend_per_share=info.get("dividendRate"),
#             dividend_yield=info.get("dividendYield"),
#             eps=info.get("trailingEps"),
#             revenue_ttm=info.get("totalRevenue"),
#             profit_margin=info.get("profitMargins"),
#             beta=info.get("beta"),
#             fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
#             fifty_two_week_low=info.get("fiftyTwoWeekLow"),
#             shares_outstanding=info.get("sharesOutstanding"),
#         )

#         return overview

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching stock overview: {str(e)}")





@router.get("/stock/fetch_bulk_overview/{ticker}", response_model=StockOverviewSchema)
async def fetch_bulk_overview(
    ticker: str, 
    session: AsyncSession = Depends(get_db),
    x_secret_key: str = Depends(verify_secret)
):
    """
    Fetch stock data from yfinance, store or update in the database, and return the overview.
    """
    try:
        # Fetch stock data from yfinance
        stock = yf.Ticker(ticker)
        info = stock.info

        # Handle case where the ticker does not exist
        if not info or "symbol" not in info:
            raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found in Yahoo Finance.")


        # Create or update StockSymbolORM
        query = select(StockSymbolORM).where(StockSymbolORM.symbol == ticker)
        result = await session.execute(query)
        existing_stock_symbol = result.scalars().first()

        if existing_stock_symbol:
            # Update existing StockSymbolORM
            existing_stock_symbol.name = info.get("shortName")
            existing_stock_symbol.exchange = info.get("exchange")
            existing_stock_symbol.currency = info.get("currency")
            existing_stock_symbol.sector = info.get("sector")
            existing_stock_symbol.industry = info.get("industry")
            stock_symbol = existing_stock_symbol
        else:
            # Create a new StockSymbolORM
            stock_symbol = StockSymbolORM(
                symbol=info.get("symbol", ticker),
                name=info.get("shortName"),
                exchange=info.get("exchange"),
                currency=info.get("currency"),
                sector=info.get("sector"),
                industry=info.get("industry"),
            )
            session.add(stock_symbol)
            await session.flush()  # Generate the ID for the new StockSymbolORM

        # Create or update StockOverviewORM
        query = (
            select(StockOverviewORM)
            .filter(StockOverviewORM.stock_symbol_id == stock_symbol.id)
            .options(joinedload(StockOverviewORM.stock_symbol))
        )
        result = await session.execute(query)
        existing_stock_overview = result.scalars().first()

        if existing_stock_overview:
            # Update existing StockOverviewORM
            existing_stock_overview.market_capitalization = info.get("marketCap")
            existing_stock_overview.book_value = info.get("bookValue")
            existing_stock_overview.trailing_pe = info.get("trailingPE")
            existing_stock_overview.forward_pe = info.get("forwardPE")
            existing_stock_overview.dividend_per_share = info.get("dividendRate")
            existing_stock_overview.dividend_yield = info.get("dividendYield")
            existing_stock_overview.eps = info.get("trailingEps")
            existing_stock_overview.revenue_ttm = info.get("totalRevenue")
            existing_stock_overview.profit_margin = info.get("profitMargins")
            existing_stock_overview.beta = info.get("beta")
            existing_stock_overview.fifty_two_week_high = info.get("fiftyTwoWeekHigh")
            existing_stock_overview.fifty_two_week_low = info.get("fiftyTwoWeekLow")
            existing_stock_overview.shares_outstanding = info.get("sharesOutstanding")
            stock_overview = existing_stock_overview
        else:
            # Create a new StockOverviewORM
            stock_overview = StockOverviewORM(
                stock_symbol_id=stock_symbol.id,
                market_capitalization=info.get("marketCap"),
                book_value=info.get("bookValue"),
                trailing_pe=info.get("trailingPE"),
                forward_pe=info.get("forwardPE"),
                dividend_per_share=info.get("dividendRate"),
                dividend_yield=info.get("dividendYield"),
                eps=info.get("trailingEps"),
                revenue_ttm=info.get("totalRevenue"),
                profit_margin=info.get("profitMargins"),
                beta=info.get("beta"),
                fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
                fifty_two_week_low=info.get("fiftyTwoWeekLow"),
                shares_outstanding=info.get("sharesOutstanding"),
            )
            session.add(stock_overview)

        # Commit changes to the database
        await session.commit()

        # Convert the ORM object to a Pydantic schema for the response
        return StockOverviewSchema.model_validate(stock_overview)

        # return StockOverviewSchema.from_orm(stock_overview)

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing stock data: {str(e)}")



@router.get("/stock/raw_balance_sheet/{ticker}")
async def get_raw_balance_sheet(ticker: str):
    """
    Fetch the balance sheet data for a given stock ticker using yfinance and return raw data.
    """
    try:
        # Fetch balance sheet data using yfinance
        stock = yf.Ticker(ticker)
        balance_sheet = stock.balance_sheet  # Annual balance sheet
        quarterly_balance_sheet = stock.quarterly_balance_sheet  # Quarterly balance sheet

        # Handle case where no balance sheet data is available
        if balance_sheet.empty and quarterly_balance_sheet.empty:
            raise HTTPException(
                status_code=404, detail=f"No balance sheet data found for ticker '{ticker}'."
            )

        # Convert pandas DataFrame to dictionaries
        annual_balance_sheet = balance_sheet.replace({np.nan: None}).to_dict()  # Replace NaN with None
        quarterly_balance_sheet = quarterly_balance_sheet.replace({np.nan: None}).to_dict()  # Replace NaN with None

        return {
            "ticker": ticker,
            "annual_balance_sheet": annual_balance_sheet,
            "quarterly_balance_sheet": quarterly_balance_sheet,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching balance sheet data: {str(e)}")


@router.get("/stock/fetch_bulk_financial_balance_reports/{ticker}", response_model=List[Any])
async def fetch_bulk_financial_reports(
    ticker: str,
    feature_type: str = Query(..., regex="^(quarterly|annual)$", description="The type of report: 'quarterly' or 'annual'"),
    session: AsyncSession = Depends(get_db),
    x_secret_key: str = Depends(verify_secret),
):

    try:

# Assuming 'info' is retrieved from Yahoo Finance as the stock's metadata
      
        query = select(StockSymbolORM.id).where(StockSymbolORM.symbol == ticker)
        result = await session.execute(query)
        stock_symbol_id = result.scalars().first()


        # Handle case where the stock symbol does not exist in the database
       # Handle case where the stock symbol does not exist
        if not stock_symbol_id:
            raise HTTPException(
                status_code=404,
                detail=f"Stock symbol '{ticker}' not found in the database. Please add it first."
            )
        stock = yf.Ticker(ticker)
        # Select balance sheet data based on the feature type
        if feature_type == "quarterly":
            balance_sheet_data = stock.quarterly_balance_sheet
        elif feature_type == "annual":
            balance_sheet_data = stock.balance_sheet
        else:
            raise ValueError("Invalid feature_type")


        # Query existing balances for the stock symbol
        query = select(FinancialBalanceORM).where(FinancialBalanceORM.stock_symbol_id == stock_symbol_id)
        result = await session.execute(query)
        existing_balances = result.scalars().all()
    # Create a set of (fiscal_date, feature_type) for quick lookup
        existing_balance_keys = {(balance.fiscal_date, balance.feature_type) for balance in existing_balances}


        balance_reports = []
        for fiscal_date, row_data in balance_sheet_data.items():
            if isinstance(fiscal_date, datetime):
                fiscal_date = fiscal_date.date()
            # Convert fiscal date to string
            # fiscal_date_as_string = str(fiscal_date.date()) if hasattr(fiscal_date, "date") else str(fiscal_date)
            
            # Check if the balance already exists
            if (fiscal_date, feature_type) in existing_balance_keys:
                continue  # Skip if the balance already exists


            snake_case_dict = convert_keys_to_snake_case(row_data.to_dict())
            snake_case_dict["stock_symbol_id"] = stock_symbol_id
            snake_case_dict["fiscal_date"] = fiscal_date
            # snake_case_dict["id"]=2
            snake_case_dict["feature_type"] = feature_type  # Add feature type to the data

            
            # Replace NaN values with None
            cleaned_dict = replace_nan_with_none(snake_case_dict)

            # Filter valid columns for the ORM model
            cleaned_dict_db = filter_valid_columns(cleaned_dict, FinancialBalanceORM)
            
            # Convert the camel_case_dict to FinanceBalanceSchema
            balance_schema = FinancialBalanceSchema(**cleaned_dict)
            new_balance = FinancialBalanceORM(**cleaned_dict_db)
            session.add(new_balance)
            await session.commit()
            balance_reports.append(balance_schema)
        return balance_reports

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing financial data: {str(e)}")