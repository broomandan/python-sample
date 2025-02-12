from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(title="Crypto pricing API using FastAPI", description="Crypto pricing API, returns list of crypto assets, returns detail of an asset")

CRYPTO_API_BASE_URL = "https://api.coingecko.com/api/v3/"
CRYPTO_API_LIST_BASE_URL = f"{CRYPTO_API_BASE_URL}simple/price?ids=bitcoin,litecoin,ethereum,ripple&vs_currencies=usd"
CRYPTO_API_DETAIL_BASE_URL = f"{CRYPTO_API_BASE_URL}coins/"

class CryptoModel(BaseModel):
     Id : str
     Symbol: str
     Name: str 
     MarketCapRank: int

class CryptoPrice(BaseModel):
    usd: float

class PriceModel(BaseModel):
    bitcoin: CryptoPrice
    ethereum: CryptoPrice
    litecoin: CryptoPrice
    ripple: CryptoPrice


@app.get("/coin_prices", response_model=PriceModel, summary="Get a list of coins")
async def get_coin_prices(
    skip: int = Query(0, description="Number of coins to skip"),
    limit: int = Query(10, description="Maximum number of coins to return"),
    name: Optional[str] = Query(None, description="Filter coins by name"),
):
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
        return None

@app.get("/coins/{coinid}", response_model=CryptoModel, summary="Get details of a specific coin")
async def get_coin_details(coinid: str):
    try:
        print(f"{CRYPTO_API_DETAIL_BASE_URL}{coinid}")
        response = requests.get(f"{CRYPTO_API_DETAIL_BASE_URL}{coinid}")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        crypto_data = {
            "Id": data["id"],
            "Symbol": data["symbol"],
            "Name": data["name"],
            "MarketCapRank": data["market_cap_rank"]
        }
        return CryptoModel(**crypto_data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    
    raise HTTPException(status_code=404, detail="Item not found")  # Raise 404 if not found


@app.exception_handler(404)
async def not_found(request, exc):
    return HTMLResponse(content="Page not found.", status_code=404)