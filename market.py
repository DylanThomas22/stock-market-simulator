import requests
import api

def get_stock(ticker):
    ticker = ticker.upper()
    try:
        ticker_response = requests.get("https://finnhub.io/api/v1/quote", 
                            params={
                                "symbol": ticker,
                                "token": api.key
                            })
    except requests.exceptions.RequestException:
        return False
    
    if ticker_response.status_code == 200:
        ticker_data = ticker_response.json()
        try:
            price = ticker_data['c']
        except KeyError:
            return False
        
        try: 
            company_response = requests.get("https://finnhub.io/api/v1/stock/profile2", 
                                        params={
                                            "symbol": ticker,
                                            "token": api.key
                                        })
        except requests.exceptions.RequestException:
            return False
        if company_response.status_code == 200:
            company_data = company_response.json()

            try:
                company_name = company_data["name"]
            except KeyError:
                return False

            return {
                "Name": company_name,
                "Price": price
            }
        else:
            return False
    else:
        return False