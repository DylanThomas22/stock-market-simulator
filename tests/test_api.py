import os
import unittest
from unittest.mock import patch

import api


class ApiConfigurationTests(unittest.TestCase):
    def test_returns_configured_key(self):
        with patch.dict(os.environ, {"FINNHUB_API_KEY": "test-key"}, clear=True):
            self.assertEqual(api.get_api_key(), "test-key")

    def test_missing_key_raises_clear_error(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "FINNHUB_API_KEY is missing"):
                api.get_api_key()


if __name__ == "__main__":
    unittest.main()
