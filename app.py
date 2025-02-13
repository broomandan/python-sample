from flask import Flask, render_template
import requests
from config import CRYPTO_API_LIST_BASE_URL, CRYPTO_API_DETAIL_BASE_URL, API_KEY_NAME, API_KEY

app = Flask(__name__)

def fetch_coin_prices(params = {
    'ids': 'bitcoin,litecoin,ethereum,ripple',
    'vs_currencies': 'usd'
}):
    try:
        headers = {API_KEY_NAME: API_KEY}
        response = requests.get(f"{CRYPTO_API_LIST_BASE_URL}", headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        print(data)
        for crypto, price_info in data.items():
            print(f"{crypto}: ${price_info['usd']}") 

        return data
    
    except requests.exceptions.RequestException as error:
        print(f'Error fetching crypto prices: {error}')
        return None
    
def fetch_coin_details(coinid):
    try:
        headers = {API_KEY_NAME: API_KEY}
        print(f"fetch: {CRYPTO_API_DETAIL_BASE_URL}{coinid}")
        response = requests.get(f"{CRYPTO_API_DETAIL_BASE_URL}{coinid}", headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None  # Or handle the error differently

@app.get("/")
def read_root():
    return ("<H1>Site is up and running</H1>")

@app.route('/coins')
def itemlist():
    items = fetch_coin_prices()
    if items:
        return render_template('coins.html', items=items)
    else:
        return render_template('error.html', message="Failed to fetch prices list.")

@app.route('/coins/<coinid>')  
def itemdetails(coinid):
    print(f"/coins/{coinid}")
    item = fetch_coin_details(f"/{coinid}") # Example endpoint; change as needed
    print(item)

    if item:
        return render_template('coindetails.html', item=item)
    else:
        return render_template('error.html', message=f"Failed to fetch details for coin {coinid}.")

@app.errorhandler(404)  # Handle 404 errors (page not found)
def page_not_found(e):
    return render_template('error.html', message="Page not found."), 404

if __name__ == '__main__':
    app.run(debug=True)


