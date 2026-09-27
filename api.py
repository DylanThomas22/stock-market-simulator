import os

from dotenv import load_dotenv


load_dotenv()


def get_api_key():
    """Return the Finnhub API key configured in the local environment."""
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise RuntimeError(
            "FINNHUB_API_KEY is missing. Copy .env.example to .env and add your key."
        )
    return api_key
