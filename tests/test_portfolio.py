import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import portfolio


def make_portfolio(balance=1000.0):
    return {
        "current_balance": balance,
        "owned_stocks": {},
        "transactions": [],
    }


class PortfolioTests(unittest.TestCase):
    def test_buy_creates_position_and_transaction(self):
        account = make_portfolio()
        quote = {"Name": "Example Corp", "Price": 100.0}

        with (
            patch("portfolio.market.get_stock", return_value=quote),
            patch("builtins.input", side_effect=["EXMP", "2"]),
            redirect_stdout(io.StringIO()),
        ):
            portfolio.buy_stock(account)

        self.assertEqual(account["current_balance"], 800.0)
        self.assertEqual(account["owned_stocks"]["EXMP"]["shares"], 2.0)
        self.assertEqual(account["transactions"][0]["type"], "BUY")

    def test_buy_updates_weighted_average_cost(self):
        account = make_portfolio()
        account["owned_stocks"]["EXMP"] = {
            "name": "Example Corp",
            "shares": 2.0,
            "average_price": 100.0,
        }
        quote = {"Name": "Example Corp", "Price": 200.0}

        with (
            patch("portfolio.market.get_stock", return_value=quote),
            patch("builtins.input", side_effect=["EXMP", "2"]),
            redirect_stdout(io.StringIO()),
        ):
            portfolio.buy_stock(account)

        self.assertEqual(account["owned_stocks"]["EXMP"]["shares"], 4.0)
        self.assertEqual(account["owned_stocks"]["EXMP"]["average_price"], 150.0)

    def test_buy_rejects_insufficient_cash(self):
        account = make_portfolio(balance=50.0)
        quote = {"Name": "Example Corp", "Price": 100.0}

        with (
            patch("portfolio.market.get_stock", return_value=quote),
            patch("builtins.input", side_effect=["EXMP", "1"]),
            redirect_stdout(io.StringIO()),
        ):
            portfolio.buy_stock(account)

        self.assertEqual(account, make_portfolio(balance=50.0))

    def test_sell_updates_cash_shares_and_realized_profit(self):
        account = make_portfolio(balance=0.0)
        account["owned_stocks"]["EXMP"] = {
            "name": "Example Corp",
            "shares": 2.0,
            "average_price": 80.0,
        }
        quote = {"Name": "Example Corp", "Price": 100.0}

        with (
            patch("portfolio.market.get_stock", return_value=quote),
            patch("builtins.input", side_effect=["EXMP", "1"]),
            redirect_stdout(io.StringIO()),
        ):
            portfolio.sell_stock(account)

        self.assertEqual(account["current_balance"], 100.0)
        self.assertEqual(account["owned_stocks"]["EXMP"]["shares"], 1.0)
        self.assertEqual(account["transactions"][0]["profit"], 20.0)

    def test_portfolio_value_handles_unavailable_market_data(self):
        account = make_portfolio()
        account["owned_stocks"]["EXMP"] = {
            "name": "Example Corp",
            "shares": 1.0,
            "average_price": 100.0,
        }

        with patch("portfolio.market.get_stock", return_value=None):
            self.assertIsNone(portfolio.calculate_portfolio_value(account))

    def test_portfolio_value_fetches_each_position_once(self):
        account = make_portfolio()
        account["owned_stocks"]["EXMP"] = {
            "name": "Example Corp",
            "shares": 2.0,
            "average_price": 100.0,
        }
        quote = {"Name": "Example Corp", "Price": 125.0}

        with patch("portfolio.market.get_stock", return_value=quote) as mock_quote:
            result = portfolio.calculate_portfolio_value(account)

        self.assertEqual(result["total_market_value"], 250.0)
        self.assertEqual(result["total_profit_loss"], 50.0)
        mock_quote.assert_called_once_with("EXMP")


if __name__ == "__main__":
    unittest.main()
