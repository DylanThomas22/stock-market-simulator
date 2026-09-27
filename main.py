import portfolio
import storage

from api import get_api_key


def login():
    while True:
        username = input("Enter login name: ").strip()
        try:
            active_portfolio = storage.load_portfolio(username)
        except ValueError as error:
            print(error)
            continue
        return username, active_portfolio


def main_menu(username, active_portfolio):
    while True:
        print(
            "\nWhat would you like to do?\n"
            "1. Buy stock\n"
            "2. Sell stock\n"
            "3. View portfolio\n"
            "4. View transaction history\n"
            "5. Quit\n"
        )

        try:
            main_menu_choice = int(input("Select an option: "))
        except ValueError:
            print("Please enter a number from 1 to 5.")
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
            print("Invalid choice. Please enter a number from 1 to 5.")


def main():
    try:
        get_api_key()
    except RuntimeError as error:
        print(error)
        return

    username, active_portfolio = login()
    main_menu(username, active_portfolio)


if __name__ == "__main__":
    main()
