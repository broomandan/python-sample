from fastapi.testclient import TestClient
import requests
from api import api

client = TestClient(api)

def test_get_coin_prices_success(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {
                "bitcoin": {"usd": 50000},
                "ethereum": {"usd": 4000}
            }
        
        @staticmethod
        def raise_for_status():
            pass

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    
    response = client.get("/coin_prices")
    assert response.status_code == 200
    assert response.json() == {
        "bitcoin": {"usd": 50000},
        "ethereum": {"usd": 4000}
    }

def test_get_coin_prices_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Error fetching crypto prices")

    monkeypatch.setattr("requests.get", mock_get)
    
    response = client.get("/coin_prices")
    assert response.status_code == 200
    assert response.json() is None
