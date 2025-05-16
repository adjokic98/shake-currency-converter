import asyncio
import aiohttp
BASE_URL = "https://api.frankfurter.dev/v1/latest"
CONVERT_URL = "https://api.frankfurter.dev/v1/latest"
HISTORICAL_URL = "https://api.frankfurter.dev/v1/"
CURRENCIES_URL = "https://api.frankfurter.dev/v1/currencies"

class ExchangeService:
    async def get_latest_rates(self, base: str = "EUR"):
        """Fetches the latest exchange rates for a given base currency."""
        params = {"base": base.upper()}
        url = BASE_URL
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get("rates")
        except aiohttp.ClientError as e:
            print(f"Error fetching latest rates: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    async def convert_currency(self, from_currency: str, to_currency: str, amount: float):
        """Converts currency using the Frankfurter API."""
        params = {"base": from_currency.upper(), "symbols": to_currency.upper()}
        url = BASE_URL
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    rate = data.get("rates", {}).get(to_currency.upper())
                    if rate is not None:
                        converted_amount = amount * rate
                        return converted_amount, rate
                    else:
                        print(f"Conversion from {from_currency} to {to_currency} failed: Rate not found.")
                        return None, None
        except aiohttp.ClientError as e:
            print(f"Error during conversion: {e}")
            return None, None
        except asyncio.TimeoutError:
            print("Timeout error during conversion.")
            return None, None
        except Exception as e:
            print(f"An unexpected error occurred during conversion: {e}")
            return None, None

    async def get_historical_rate(self, base: str, target: str, date: str):
        """Fetches historical rates using the Frankfurter API."""
        url = f"{HISTORICAL_URL}{date}?base={base.upper()}&symbols={target.upper()}"
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    rate = data.get("rates", {}).get(target.upper())
                    return rate
        except aiohttp.ClientError as e:
            print(f"Error fetching historical rate: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred fetching historical rate: {e}")
            return None

    async def get_supported_currencies(self) -> dict | None:
        """Fetches the list of supported currencies from the Frankfurter API."""
        url = CURRENCIES_URL
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error fetching supported currencies: {e}")
            return None
        except asyncio.TimeoutError:
            print("Timeout error fetching supported currencies.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred fetching supported currencies: {e}")
            return None