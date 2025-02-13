from typing import Optional
from fastapi import APIRouter,  Query
from config import CRYPTO_API_LIST_BASE_URL, CRYPTO_API_DETAIL_BASE_URL
from models.models import CryptoModel, PriceModel
import requests

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "API is up and running"}

@router.get("/coin_prices", response_model=PriceModel, summary="Get a list of coins")
async def get_coin_prices(
    skip: int = Query(0, description="Number of coins to skip"),
    limit: int = Query(10, description="Maximum number of coins to return"),
    name: Optional[str] = Query(None, description="Filter coins by name"),
):
    response = requests.get(f"{CRYPTO_API_LIST_BASE_URL}")
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    data = response.json()
    print(data)
    for crypto, price_info in data.items():
        print(f"{crypto}: ${price_info['usd']}") 

    return data
@router.get("/coins/{coinid}", response_model=CryptoModel, summary="Get details of a specific coin")
async def get_coin_details(coinid: str):
    print(f"{CRYPTO_API_DETAIL_BASE_URL}{coinid}")
    response = requests.get(f"{CRYPTO_API_DETAIL_BASE_URL}{coinid}")
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    data = response.json()
    crypto_instance = CryptoModel(
        id=data["id"],
        symbol=data["symbol"],
        name=data["name"],
        market_cap_rank=data["market_cap_rank"]
    )
    return crypto_instance