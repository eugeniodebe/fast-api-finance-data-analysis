from pydantic import BaseModel
from typing import Optional


class StockSymbolSchema(BaseModel):
    id: Optional[int] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "exchange": "NASDAQ",
                "currency": "USD",
                "sector": "Technology",
                "industry": "Consumer Electronics"
            }
        }
