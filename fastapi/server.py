from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db import read_all_items, update_item  # Importer la fonction depuis db.py
import httpx

# Importer la fonction get_connection depuis utils.py
from config import get_db

# Créer une instance de l'application FastAPI
app = FastAPI(
    title="FastAPI Starter",
    description="Un point de départ pour une application FastAPI",
    version="1.0.0",
)

# Modèle Pydantic pour les requêtes/réponses
class Item(BaseModel):
    cryptoid: int
    cryptoname: str
    coingeckoid: str
    alert1: float 
    alert2: float 
    alert3: float 
    lastprice: float 
    amount: float 
    total: float 

    class Config:
        orm_mode = True

# Route d'accueil
@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API FastAPI Starter avec PostgreSQL!"}

# Route pour récupérer tous les items
@app.get("/items", response_model=List[Item])
async def get_all_items_route(db: AsyncSession = Depends(get_db)):
    items = await read_all_items(db)
    return items

# Fonction pour récupérer les prix des cryptomonnaies
async def get_crypto_prices(cryptos: List[str] = ["bitcoin", "ethereum", "litecoin"]):
    """
    Récupère les prix actuels d'une liste de cryptomonnaies depuis l'API CoinGecko.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(cryptos),  # Liste des cryptomonnaies séparées par des virgules
        "vs_currencies": "usd",   # Devise de conversion (USD)
    }
    headers = { 'x-cg-demo-api-key': 'CG-aR9bPtBpq5uXZYgmo7xvaQzp' }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erreur lors de l'appel à l'API CoinGecko")

    return response.json()


# Route principale 
@app.get("/main")
async def main_route(db: AsyncSession = Depends(get_db)):
    """
    Route principale qui récupère les items depuis la base de données,
    les prix des cryptomonnaies correspondantes, et effectue des calculs et mises à jour.
    """
    # Appeler la fonction read_all_items pour récupérer les items
    items = await read_all_items(db)

    # Trace console pour afficher les items récupérés
    print("=== Items Récupérés ===")
    print(items)

    # Extraire les valeurs de 'coingeckoid' depuis les items
    cryptos = [item.coingeckoid for item in items]
    # Trace console pour afficher les cryptos extraites
    print("=== Cryptos ===")
    print(cryptos)

    # Appeler la fonction get_crypto_prices avec la liste des cryptomonnaies
    crypto_prices = await get_crypto_prices(cryptos)
    # Trace console pour afficher crypto_prices
    print("=== Crypto Prices ===")
    print(crypto_prices)

    # Initialiser une liste pour stocker les alertes
    alerts = []

   # Initialiser la somme totale
    crypto_total = 0

    # Parcourir les items et effectuer les calculs
    for item in items:
        # Récupérer le prix USD depuis l'API CoinGecko
        price_usd = crypto_prices.get(item.coingeckoid, {}).get("usd", 0)

        # Calculer la valeur totale (amount * usd)
        total = item.amount * price_usd if item.amount else 0
        # Ajouter au total global
        crypto_total += total

        # Mettre à jour la valeur lastprice dans la base de données
        await update_item(db, int(item.cryptoid), {"lastprice": price_usd})
        await update_item(db, int(item.cryptoid), {"total": total})

        # Comparer le prix avec les alertes
        if item.alert3 and price_usd >= item.alert3:
            alerts.append(f"Crypto {item.cryptoname} a atteint l'alerte 3 avec un prix de {price_usd} USD")
        elif item.alert2 and price_usd >= item.alert2:
            alerts.append(f"Crypto {item.cryptoname} a atteint l'alerte 2 avec un prix de {price_usd} USD")
        elif item.alert1 and price_usd >= item.alert1:
            alerts.append(f"Crypto {item.cryptoname} a atteint l'alerte 1 avec un prix de {price_usd} USD")

    print("=== Fin de la boucle ===")
    print(f"Total des cryptos : {crypto_total}")
    print(f"Alertes générées : {alerts}")

    # Retourner les items et les prix des cryptomonnaies
    return {
        "crypto_prices": crypto_prices,
        "alerts": alerts,
        "cryptototal": crypto_total
    }


