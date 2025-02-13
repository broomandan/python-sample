from pydantic import BaseModel

class CryptoModel(BaseModel):
    id: str
    symbol: str
    name: str 
    market_cap_rank: int

class CryptoPrice(BaseModel):
    usd: float

class PriceModel(BaseModel):
    bitcoin: CryptoPrice
    ethereum: CryptoPrice
    litecoin: CryptoPrice
    ripple: CryptoPrice