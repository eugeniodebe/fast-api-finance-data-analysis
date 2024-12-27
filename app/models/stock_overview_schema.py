from pydantic import BaseModel
from typing import Optional
from app.models.stock_symbol_schema import StockSymbolSchema


class StockOverviewSchema(BaseModel):
    id: Optional[int] = None
    stock_symbol: Optional[StockSymbolSchema] = None
    market_capitalization: Optional[int] = None
    book_value: Optional[float] = None
    trailing_pe: Optional[float] = None
    forward_pe: Optional[float] = None
    dividend_per_share: Optional[float] = None
    dividend_yield: Optional[float] = None
    eps: Optional[float] = None
    revenue_ttm: Optional[int] = None
    profit_margin: Optional[float] = None
    beta: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    shares_outstanding: Optional[int] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "stock_symbol": {
                    "id": 1,
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "exchange": "NASDAQ",
                    "currency": "USD",
                    "sector": "Technology",
                    "industry": "Consumer Electronics"
                },
                "market_capitalization": 2000000000000,
                "book_value": 3.5,
                "trailing_pe": 25.6,
                "forward_pe": 22.1,
                "dividend_per_share": 0.82,
                "dividend_yield": 0.015,
                "eps": 6.5,
                "revenue_ttm": 365817000000,
                "profit_margin": 0.21,
                "beta": 1.2,
                "fifty_two_week_high": 157.26,
                "fifty_two_week_low": 116.21,
                "shares_outstanding": 17000000000
            }
        }
