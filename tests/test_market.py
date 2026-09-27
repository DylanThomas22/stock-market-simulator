import unittest
from unittest.mock import Mock, call, patch

import requests

import market


class MarketTests(unittest.TestCase):
    @patch("market.get_api_key", return_value="test-key")
    @patch("market.requests.get")
    def test_get_stock_returns_normalized_quote(self, mock_get, _mock_key):
        quote_response = Mock()
        quote_response.json.return_value = {"c": 125.5}
        profile_response = Mock()
        profile_response.json.return_value = {"name": "Example Corp"}
        mock_get.side_effect = [quote_response, profile_response]

        result = market.get_stock("exmp")

        self.assertEqual(result, {"Name": "Example Corp", "Price": 125.5})
        self.assertEqual(
            mock_get.call_args_list,
            [
                call(
                    market.QUOTE_URL,
                    params={"symbol": "EXMP", "token": "test-key"},
                    timeout=market.REQUEST_TIMEOUT,
                ),
                call(
                    market.PROFILE_URL,
                    params={"symbol": "EXMP", "token": "test-key"},
                    timeout=market.REQUEST_TIMEOUT,
                ),
            ],
        )

    @patch("market.get_api_key", return_value="test-key")
    @patch(
        "market.requests.get",
        side_effect=requests.exceptions.Timeout,
    )
    def test_get_stock_returns_none_on_network_failure(self, _mock_get, _mock_key):
        self.assertIsNone(market.get_stock("EXMP"))

    @patch("market.get_api_key", return_value="test-key")
    @patch("market.requests.get")
    def test_get_stock_rejects_zero_price(self, mock_get, _mock_key):
        quote_response = Mock()
        quote_response.json.return_value = {"c": 0}
        profile_response = Mock()
        profile_response.json.return_value = {"name": "Example Corp"}
        mock_get.side_effect = [quote_response, profile_response]

        self.assertIsNone(market.get_stock("EXMP"))


if __name__ == "__main__":
    unittest.main()
