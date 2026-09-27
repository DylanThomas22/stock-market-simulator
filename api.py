import os

from dotenv import load_dotenv

load_dotenv()

key = os.getenv("FINNHUB_API_KEY")

if not key:
    raise RuntimeError(
        "FINNHUB_API_KEY is missing. Add it to your .env file."
    )