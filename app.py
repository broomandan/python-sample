from flask import Flask, render_template
import requests

app = Flask(__name__)

# Replace with your actual API endpoint
# API_BASE_URL = "https://jsonplaceholder.typicode.com"  # Example: JSONPlaceholder
CRYPTO_API_LIST_BASE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,litecoin,ethereum,ripple&vs_currencies=usd"  
CRYPTO_API_DETAIL_BASE_URL = "https://api.coingecko.com/api/v3/"  


# Sample API data structure (adapt to your API's actual structure)
# This is just an example; your API will likely return different data
# It's important to understand the structure of the JSON your API returns
# so you can access the correct fields in your templates.

# Example of a function to fetch data from the API
def fetch_data(params = {
    'ids': 'bitcoin,litecoin,ethereum,ripple',
    'vs_currencies': 'usd'
}):
    try:
        response = requests.get(f"{CRYPTO_API_LIST_BASE_URL}")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        print(data)
        for crypto, price_info in data.items():
            print(f"{crypto}: ${price_info['usd']}") 

        return data
    
    except requests.exceptions.RequestException as error:
        print(f'Error fetching crypto prices: {error}')
    
def fetch_itemDetails(coinid):
    try:
        print(f"{CRYPTO_API_DETAIL_BASE_URL}{coinid}")
        response = requests.get(f"{CRYPTO_API_DETAIL_BASE_URL}{coinid}")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None  # Or handle the error differently

@app.route('/itemlist')
def itemlist():
    #items = fetch_data("/todos") # Example endpoint; change as needed
    items =fetch_data()
    if items:
       # print(items) # For debugging
        return render_template('itemlist.html', items=items)
    else:
        return render_template('error.html', message="Failed to fetch item list.")


@app.route('/itemdetails/<item_id>')  # <int:item_id> makes item_id an integer
def itemdetails(item_id):
    print(f"/coins/{item_id}")
    item = fetch_itemDetails(f"/coins/{item_id}") # Example endpoint; change as needed

    if item:
        return render_template('itemdetails.html', item=item)
    else:
        return render_template('error.html', message=f"Failed to fetch details for item {item_id}.")


@app.errorhandler(404)  # Handle 404 errors (page not found)
def page_not_found(e):
    return render_template('error.html', message="Page not found."), 404

if __name__ == '__main__':
    app.run(debug=True)


# assdas 


