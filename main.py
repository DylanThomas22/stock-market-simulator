import portfolio
import storage
import market

def login():
    username = input("Enter Login Name: ")
    active_portfolio = storage.load_portfolio(username)
    return username, active_portfolio

def main_menu(username, active_portfolio):

    while True:
        print("What option would you like to select:\n"
                  "1.Buy Stock\n"
                  "2.Sell Stock\n"
                  "3.View Portfolio\n"
                  "4.View Transaction History\n"
                  "5.Quit\n")
            

        try:
            main_menu_choice = int(input())
        except ValueError:
            print("Please enter a number")
            continue

        if main_menu_choice == 1:
            portfolio.buy_stock(active_portfolio)
            storage.save_portfolio(username, active_portfolio)
        elif main_menu_choice == 2:
            portfolio.sell_stock(active_portfolio)
            storage.save_portfolio(username, active_portfolio)
        elif main_menu_choice == 3:
            portfolio.view_portfolio(active_portfolio)
        elif main_menu_choice == 4:
            portfolio.transaction_history(active_portfolio)
        elif main_menu_choice == 5:
            print("Thank you, goodbye!")
            break
        else:
            print("Invalid Choice")
            
        
    
username, active_portfolio = login()
main_menu(username, active_portfolio)