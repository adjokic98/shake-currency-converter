from fastapi import APIRouter, HTTPException, Depends
from schemas.currency import SupportedCurrenciesResponse, ConversionRequest, ConversionResponse
from db.operations import get_supported_currencies, decrement_user_credits
from services.exchange import ExchangeService
from utils.dependencies import rate_limit_by_credits

router = APIRouter(prefix="/currency", tags=["currency"])
exchange_service = ExchangeService()

@router.get("/currencies", response_model=SupportedCurrenciesResponse)
async def list_currencies(user_data: dict = Depends(rate_limit_by_credits)):
    """Lists all supported currencies (consumes a credit)."""
    currencies = await get_supported_currencies()
    return {"currencies": currencies}

@router.post("/convert", response_model=ConversionResponse, dependencies=[Depends(rate_limit_by_credits)])
async def convert_currency(
    conversion_request: ConversionRequest,
    user_data: dict = Depends(rate_limit_by_credits)
):
    """Converts currency from one type to another, with optional historical data.
    Deducts credits only on successful conversion.
    """
    base_currency = conversion_request.base_currency.upper()
    target_currency = conversion_request.target_currency.upper()
    amount = conversion_request.amount
    date = conversion_request.date
    user_email = user_data.get("email")

    supported_currencies_list = await get_supported_currencies()
    if base_currency not in supported_currencies_list or target_currency not in supported_currencies_list:
        raise HTTPException(status_code=400, detail="Invalid currency code(s)")

    converted_amount = None
    rate = None

    try:
        if date:
            rate = await exchange_service.get_historical_rate(base_currency, target_currency, date)
            if rate is not None:
                converted_amount = amount * rate
            else:
                raise HTTPException(status_code=400, detail=f"Historical data not available for {base_currency}/{target_currency} on {date}")
        else:
            converted_amount, rate = await exchange_service.convert_currency(base_currency, target_currency, amount)
            if converted_amount is None:
                raise HTTPException(status_code=400, detail=f"Could not convert {base_currency} to {target_currency}")

        # Deduct credits only if the conversion was successful
        decrement_user_credits(user_email)
        return ConversionResponse(
            base_currency=base_currency,
            target_currency=target_currency,
            amount=amount,
            converted_amount=converted_amount,
            rate=rate,
            date=date
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed due to an unexpected error: {e}")