import asyncio
from db.data import users
from services.exchange import ExchangeService

exchange_service = ExchangeService()
supported_currencies_cache = None
supported_currencies_cache_time = None
CACHE_EXPIRATION_TIME = 3600  # Cache for 1 hour (in seconds)

async def fetch_and_cache_supported_currencies():
    """Fetches supported currencies from the API and caches them."""
    global supported_currencies_cache, supported_currencies_cache_time
    currencies = await exchange_service.get_supported_currencies()
    if currencies:
        supported_currencies_cache = set(currencies.keys())
        supported_currencies_cache_time = asyncio.get_event_loop().time()
        return True
    return False

async def get_supported_currencies() -> list[str]:
    """Retrieves the list of supported currencies, using the cache if valid."""
    global supported_currencies_cache, supported_currencies_cache_time
    current_time = asyncio.get_event_loop().time()
    if supported_currencies_cache and supported_currencies_cache_time and (current_time - supported_currencies_cache_time < CACHE_EXPIRATION_TIME):
        return sorted(list(supported_currencies_cache))
    else:
        if await fetch_and_cache_supported_currencies():
            return sorted(list(supported_currencies_cache))
        else:
            return [] # Return empty list because API is not available

def get_user_by_email(email: str) -> dict | None:
    return users.get(email)

def get_user_by_api_key(api_key: str) -> dict | None:
    for _, user_data in users.items():
        if user_data.get("api_key") == api_key:
            return user_data
    return None

def create_user(email: str, api_key: str, initial_credits: int = 100):
    users[email] = {"api_key": api_key, "credits": initial_credits, "email": email}

def update_user_credits(email: str, amount: int):
    if email in users:
        users[email]["credits"] += amount

def decrement_user_credits(email: str) -> bool:
    if email in users and users[email]["credits"] > 0:
        users[email]["credits"] -= 1
        return True
    return False

def get_user_credits(email: str) -> int | None:
    if email in users:
        return users[email]["credits"]
    return None