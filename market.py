import requests

from api import get_api_key


QUOTE_URL = "https://finnhub.io/api/v1/quote"
PROFILE_URL = "https://finnhub.io/api/v1/stock/profile2"
REQUEST_TIMEOUT = 10


def get_stock(ticker):
    """Return the latest price and company name for a ticker, or None on failure."""
    ticker = ticker.strip().upper()
    if not ticker:
        return None

    request_params = {
        "symbol": ticker,
        "token": get_api_key(),
    }

    try:
        ticker_response = requests.get(
            QUOTE_URL,
            params=request_params,
            timeout=REQUEST_TIMEOUT,
        )
        ticker_response.raise_for_status()
        ticker_data = ticker_response.json()
        price = ticker_data.get("c")

        company_response = requests.get(
            PROFILE_URL,
            params=request_params,
            timeout=REQUEST_TIMEOUT,
        )
        company_response.raise_for_status()
        company_data = company_response.json()
        company_name = company_data.get("name")
    except (requests.exceptions.RequestException, ValueError, TypeError):
        return None

    if not isinstance(price, (int, float)) or price <= 0 or not company_name:
        return None

    return {
        "Name": company_name,
        "Price": float(price),
    }
