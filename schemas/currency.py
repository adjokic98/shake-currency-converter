from pydantic import BaseModel
from typing import List, Dict, Optional

class SupportedCurrenciesResponse(BaseModel):
    currencies: List[str]

class ConversionRequest(BaseModel):
    base_currency: str
    target_currency: str
    amount: float
    date: Optional[str] = None  # For historical data

class ConversionResponse(BaseModel):
    base_currency: str
    target_currency: str
    amount: float
    converted_amount: float
    rate: float
    date: Optional[str] = None