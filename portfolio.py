import market


def buy_stock(active_portfolio):
    ticker = input("Enter a ticker: ").strip().upper()
    stock = market.get_stock(ticker)
    if not stock:
        print("Ticker not found or market data is unavailable.")
        return active_portfolio

    print(f"Current price of {stock['Name']} is ${stock['Price']:,.2f}.")
    try:
        purchased_shares = float(input("How many shares would you like to buy? "))
    except ValueError:
        print("Please enter a valid number.")
        return active_portfolio

    if purchased_shares <= 0:
        print("Shares must be greater than 0.")
        return active_portfolio

    total_cost = purchased_shares * stock["Price"]
    if total_cost > active_portfolio["current_balance"]:
        print("Balance too low!")
        return active_portfolio

    if ticker in active_portfolio["owned_stocks"]:
        owned_stock = active_portfolio["owned_stocks"][ticker]
        old_investment = owned_stock["average_price"] * owned_stock["shares"]
        new_investment = stock["Price"] * purchased_shares

        owned_stock["average_price"] = (
            old_investment + new_investment
        ) / (owned_stock["shares"] + purchased_shares)
        owned_stock["shares"] += purchased_shares
    else:
        active_portfolio["owned_stocks"][ticker] = {
            "name": stock["Name"],
            "shares": purchased_shares,
            "average_price": stock["Price"],
        }

    active_portfolio["current_balance"] -= total_cost
    active_portfolio["transactions"].append(
        {
            "type": "BUY",
            "ticker": ticker,
            "shares": purchased_shares,
            "price": stock["Price"],
            "total": total_cost,
        }
    )

    print(
        f"Bought {purchased_shares:g} shares of {ticker} for ${total_cost:,.2f}."
    )
    print(f"Remaining cash: ${active_portfolio['current_balance']:,.2f}")
    return active_portfolio


def calculate_position_value(ticker, stock):
    market_stock = market.get_stock(ticker)
    if not market_stock:
        return None

    current_price = market_stock["Price"]
    owned_shares = stock["shares"]
    average_price = stock["average_price"]
    current_value = current_price * owned_shares
    original_cost = average_price * owned_shares

    return {
        "current_price": current_price,
        "current_value": current_value,
        "original_cost": original_cost,
        "unrealized_profit_loss": current_value - original_cost,
    }


def calculate_portfolio_value(active_portfolio):
    position_values = {}
    total_current_value = 0
    total_original_cost = 0
    total_profit_loss = 0

    for ticker, stock in active_portfolio["owned_stocks"].items():
        values = calculate_position_value(ticker, stock)
        if values is None:
            return None

        position_values[ticker] = values
        total_current_value += values["current_value"]
        total_original_cost += values["original_cost"]
        total_profit_loss += values["unrealized_profit_loss"]

    return {
        "positions": position_values,
        "total_market_value": total_current_value,
        "total_cost": total_original_cost,
        "total_profit_loss": total_profit_loss,
    }


def view_portfolio(active_portfolio):
    print("\n========== PORTFOLIO ==========")
    print(f"Cash Balance: ${active_portfolio['current_balance']:,.2f}\n")

    if not active_portfolio["owned_stocks"]:
        print("You don't own any stocks.")
        return True

    portfolio_summary = calculate_portfolio_value(active_portfolio)
    if portfolio_summary is None:
        print("Unable to calculate portfolio value because market data is unavailable.")
        return False

    print(
        f"{'Ticker':<8} | "
        f"{'Company':<20} | "
        f"{'Shares':>10} | "
        f"{'Avg Cost':>12} | "
        f"{'Current':>12} | "
        f"{'Value':>12} | "
        f"{'Cost Basis':>12} | "
        f"{'Unrealized P/L':>15}"
    )
    print("-" * 124)

    for ticker, stock in active_portfolio["owned_stocks"].items():
        position_value = portfolio_summary["positions"][ticker]
        print(
            f"{ticker:<8} | "
            f"{stock['name'][:20]:<20} | "
            f"{stock['shares']:>10.2f} | "
            f"${stock['average_price']:>11,.2f} | "
            f"${position_value['current_price']:>11,.2f} | "
            f"${position_value['current_value']:>11,.2f} | "
            f"${position_value['original_cost']:>11,.2f} | "
            f"${position_value['unrealized_profit_loss']:>14,.2f}"
        )

    print("-" * 124)
    print(f"Total Positions:      {len(active_portfolio['owned_stocks'])}")
    print(f"Total Invested:       ${portfolio_summary['total_cost']:,.2f}")
    print(f"Current Stock Value:  ${portfolio_summary['total_market_value']:,.2f}")
    print(f"Unrealized P/L:       ${portfolio_summary['total_profit_loss']:,.2f}")
    print(f"Cash Balance:         ${active_portfolio['current_balance']:,.2f}")
    print(
        "Total Account Value:  "
        f"${active_portfolio['current_balance'] + portfolio_summary['total_market_value']:,.2f}"
    )
    return True


def sell_stock(active_portfolio):
    if not active_portfolio["owned_stocks"]:
        print("You don't own any stocks.")
        return active_portfolio

    print("Here are your current stocks.")
    if not view_portfolio(active_portfolio):
        return active_portfolio

    sell_ticker = input("Enter the ticker you'd like to sell: ").strip().upper()
    if sell_ticker not in active_portfolio["owned_stocks"]:
        print("You do not own this stock.")
        return active_portfolio

    owned_stock = active_portfolio["owned_stocks"][sell_ticker]
    try:
        shares_to_sell = float(input("How many shares would you like to sell? "))
    except ValueError:
        print("Please enter a valid number.")
        return active_portfolio

    if shares_to_sell <= 0:
        print("Shares must be greater than 0.")
        return active_portfolio
    if shares_to_sell > owned_stock["shares"]:
        print("You do not have enough shares.")
        return active_portfolio

    market_stock = market.get_stock(sell_ticker)
    if not market_stock:
        print("Stock data unavailable.")
        return active_portfolio

    sale_value = shares_to_sell * market_stock["Price"]
    sale_profit = (
        market_stock["Price"] - owned_stock["average_price"]
    ) * shares_to_sell

    active_portfolio["current_balance"] += sale_value
    owned_stock["shares"] -= shares_to_sell
    if owned_stock["shares"] <= 0:
        del active_portfolio["owned_stocks"][sell_ticker]

    active_portfolio["transactions"].append(
        {
            "type": "SELL",
            "ticker": sell_ticker,
            "shares": shares_to_sell,
            "price": market_stock["Price"],
            "total": sale_value,
            "profit": sale_profit,
        }
    )

    print(f"Sold {shares_to_sell:g} shares of {sell_ticker}.")
    print(f"Sale Value: ${sale_value:,.2f}")
    print(f"Realized P/L: ${sale_profit:,.2f}")
    return active_portfolio


def transaction_history(active_portfolio):
    print("\n========== TRANSACTION HISTORY ==========")
    if not active_portfolio["transactions"]:
        print("No transactions recorded yet.")
        return

    for transaction in active_portfolio["transactions"]:
        if transaction["type"] == "BUY":
            print(
                f"BUY  | {transaction['ticker']} | "
                f"{transaction['shares']:g} shares @ ${transaction['price']:,.2f} | "
                f"Total: ${transaction['total']:,.2f}"
            )
        else:
            print(
                f"SELL | {transaction['ticker']} | "
                f"{transaction['shares']:g} shares @ ${transaction['price']:,.2f} | "
                f"Total: ${transaction['total']:,.2f} | "
                f"P/L: ${transaction['profit']:,.2f}"
            )
