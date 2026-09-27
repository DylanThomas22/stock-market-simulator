import os
import json

def default_portfolio():
    portfolio = {
    "current_balance": 100000,
    "owned_stocks": {},
    "transactions": []
}
    return portfolio

def load_portfolio(username):
    file_path = f"users/{username}/portfolio.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            loaded_portfolio = json.load(file)
        return loaded_portfolio
    else:
        loaded_portfolio = default_portfolio()
        save_portfolio(username, loaded_portfolio)
        return loaded_portfolio



def save_portfolio(username, portfolio):
    file_path = f"users/{username}/portfolio.json"
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(file_path, "w") as file:
        json.dump(portfolio, file)