from fastapi.testclient import TestClient
from fastapi_app.server import app  # Assure-toi que le fichier s'appelle main.py

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue dans l'API FastAPI Starter avec PostgreSQL!"}

def test_get_all_items_route(monkeypatch):
    # Mock de la fonction read_all_items
    def mock_read_all_items():
        return [{"cryptoid": 1, "cryptoname": "Bitcoin", "coingeckoid": "bitcoin"}]

    monkeypatch.setattr("main.read_all_items", mock_read_all_items)

    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["cryptoname"] == "Bitcoin"

def test_top5_route(monkeypatch):
    def mock_get_top5_cryptos():
        return [{"cryptoname": "Bitcoin", "total": 10000}, {"cryptoname": "Ethereum", "total": 8000}]

    monkeypatch.setattr("main.get_top5_cryptos", mock_get_top5_cryptos)

    response = client.get("/top5")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["cryptoname"] == "Bitcoin"
