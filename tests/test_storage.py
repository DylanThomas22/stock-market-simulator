import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import storage


class StorageTests(unittest.TestCase):
    def test_portfolio_round_trip(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            users_directory = Path(temporary_directory) / "users"
            with patch.object(storage, "USERS_DIR", users_directory):
                account = storage.load_portfolio("test_user")
                account["current_balance"] = 97500
                storage.save_portfolio("test_user", account)

                loaded_account = storage.load_portfolio("test_user")

        self.assertEqual(loaded_account["current_balance"], 97500)

    def test_rejects_unsafe_username(self):
        with self.assertRaises(ValueError):
            storage.portfolio_path("../../outside")


if __name__ == "__main__":
    unittest.main()
