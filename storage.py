import json
import re
from pathlib import Path


USERS_DIR = Path("users")
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,32}$")


def default_portfolio():
    return {
        "current_balance": 100000,
        "owned_stocks": {},
        "transactions": [],
    }


def portfolio_path(username):
    username = username.strip()
    if not USERNAME_PATTERN.fullmatch(username):
        raise ValueError(
            "Login names must be 1-32 characters and contain only letters, "
            "numbers, hyphens, or underscores."
        )
    return USERS_DIR / username / "portfolio.json"


def load_portfolio(username):
    file_path = portfolio_path(username)
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    portfolio = default_portfolio()
    save_portfolio(username, portfolio)
    return portfolio


def save_portfolio(username, portfolio):
    file_path = portfolio_path(username)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = file_path.with_suffix(".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(portfolio, file, indent=2)
    temporary_path.replace(file_path)
