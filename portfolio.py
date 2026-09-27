import market
import json

def buy_stock(active_portfolio):
    ticker = input("Enter Valid Ticker: ").upper()
    stock = market.get_stock(ticker)
    if stock:
        print(f"Current price of {stock['Name']} is ${stock['Price']}\n")
        try:
            purchased_shares = float(input("How many shares would you like to buy? "))
        except ValueError:
            print("Please enter a valid number.")
            return

        if purchased_shares <= 0:
            print("Shares must be greater than 0.")
            return

        total_cost = purchased_shares * stock["Price"]
        if total_cost <= active_portfolio["current_balance"]:
            

            if ticker in active_portfolio["owned_stocks"]:
                old_shares = active_portfolio["owned_stocks"][ticker]["shares"]
                old_price = active_portfolio["owned_stocks"][ticker]["average_price"]
                old_investment = old_price * old_shares

                new_price = stock["Price"]
                new_investment = new_price * purchased_shares

                active_portfolio["owned_stocks"][ticker]["average_price"] = (
                    (old_investment) + (new_investment)
                ) / (old_shares + purchased_shares)

                active_portfolio["owned_stocks"][ticker]["shares"] += purchased_shares
            else:
                active_portfolio["owned_stocks"][ticker] = {
                    "name": stock["Name"],
                    "shares": purchased_shares,
                    "average_price": stock["Price"]
                }
            print(f"Successfully bought {purchased_shares} of {ticker} for {total_cost}\n")
            
            active_portfolio["current_balance"] -= total_cost
            print(f"You have {active_portfolio['current_balance']:.2f} remaining.")

            buy_record = {
                "type": "BUY",
                "ticker": ticker,
                "shares": purchased_shares,
                "price": stock["Price"],
                "total": total_cost
            }
            active_portfolio["transactions"].append(buy_record)

            
        else:
            print("Balance too low!")      
    else:
        print("Ticker not found")
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
    unrealized_pl = current_value - original_cost
    return {
            "current_price": current_price,
            "current_value": current_value,
            "original_cost": original_cost,
            "unrealized_profit_loss": unrealized_pl
        }
    
def calculate_portfolio_value(active_portfolio):
    total_current_value = 0
    total_original_cost = 0
    total_pl = 0
    for ticker, stock in active_portfolio["owned_stocks"].items():
        values = calculate_position_value(ticker, stock)
        if values is None:
            return None

        total_current_value += values["current_value"]
        total_original_cost += values["original_cost"]
        total_pl += values["unrealized_profit_loss"]
    return {
        "total_market_value": total_current_value,
        "total_cost": total_original_cost,
        "total_profit_loss": total_pl
    }

def view_portfolio(active_portfolio):
    print("========== PORTFOLIO ==========\n")
    print()
    print(f"Cash Balance: ${active_portfolio['current_balance']:.2f}\n")
    if active_portfolio['owned_stocks']:
        print(
            f"{'Ticker':<8} | "
            f"{'Company':<20} | "
            f"{'Shares':<10} | "
            f"{'Avg Cost':<12} | "
            f"{'Current':<12} | "
            f"{'Value':<12} | "
            f"{'Cost Basis':<12} | "
            f"{'Unrealized P/L':<15}"
        )

        print("-" * 115)

        for ticker, stock in active_portfolio["owned_stocks"].items():
            position_value = calculate_position_value(ticker, stock)
            if position_value is None:
                print(f"Market data unavailable for {ticker}. Please try again later.")
                return

            print(
                f"{ticker:<8} | "
                f"{stock['name']:<20} | "
                f"{stock['shares']:<10.2f} | "
                f"${stock['average_price']:<11.2f} | "
                f"${position_value['current_price']:<11.2f} | "
                f"${position_value['current_value']:<11.2f} | "
                f"${position_value['original_cost']:<11.2f} | "
                f"${position_value['unrealized_profit_loss']:<14.2f}"
            )

        portfolio_summary = calculate_portfolio_value(active_portfolio)
        if portfolio_summary is None:
            print("Unable to calculate portfolio totals because market data is unavailable.")
            return

        print("-" * 115)
        print(f"Total Positions: {len(active_portfolio['owned_stocks'])}")
        print(f"Total Invested:       ${portfolio_summary['total_cost']:.2f}")
        print(f"Current Stock Value:  ${portfolio_summary['total_market_value']:.2f}")
        print(f"Unrealized P/L:       ${portfolio_summary['total_profit_loss']:.2f}")
        print(f"Cash Balance:         ${active_portfolio['current_balance']:.2f}")
        print(f"Total Account Value:  ${(active_portfolio['current_balance'] + portfolio_summary['total_market_value']):.2f}\n")
    else:
        print("You don't own any stocks.")

def sell_stock(active_portfolio):
    print("Here are your current stocks.")
    view_portfolio(active_portfolio)

    sell_ticker = input("Enter the ticker you'd like to sell: ").upper()
    if sell_ticker in active_portfolio["owned_stocks"]:
        owned_stock = active_portfolio["owned_stocks"][sell_ticker]

        try:
            shares_to_sell = float(input("How many shares would you like to sell? "))
        except ValueError:
            print("Please enter a valid number.")
            return
        if shares_to_sell <= 0:
            print("Shares must be greater than 0.")
            return
        if shares_to_sell > owned_stock['shares']:
            print("You do not have enough shares.")
            return
        
        market_stock = market.get_stock(sell_ticker)
        if not market_stock:
            print("Stock data unavailable.")
            return
        
        sale_value = shares_to_sell * market_stock['Price']
        sale_profit = (
                        market_stock["Price"] - owned_stock["average_price"]
                    ) * shares_to_sell
        print(f"Selling {shares_to_sell} of {sell_ticker}\n"
              f"Sale Value: ${sale_value:.2f}\n"
              f"Profit/Loss ${sale_profit:.2f}\n")
        
        active_portfolio["current_balance"] += sale_value
        owned_stock["shares"] -= shares_to_sell
        if active_portfolio["owned_stocks"][sell_ticker]['shares'] <= 0:
            del active_portfolio["owned_stocks"][sell_ticker]

        sell_record = {
            'type': 'SELL',
            'ticker': sell_ticker,
            'shares': shares_to_sell,
            'price': market_stock["Price"],
            'total': sale_value,
            'profit': sale_profit
        }
        active_portfolio["transactions"].append(sell_record)

    else:
        print("You do not own this stock.")

def transaction_history(active_portfolio):
    print("========== TRANSACTION HISTORY ==========")
    if not active_portfolio["transactions"]:
        print("No transactions recorded yet.")
        return

    for tx in active_portfolio["transactions"]:
        if tx["type"] == "BUY":
            print(f"BUY  | {tx['ticker']} | {tx['shares']} shares @ ${tx['price']:.2f} | Total: ${tx['total']:.2f}")
        else:
            print(f"SELL | {tx['ticker']} | {tx['shares']} shares @ ${tx['price']:.2f} | Total: ${tx['total']:.2f} | P&L: ${tx['profit']:.2f}")
    
