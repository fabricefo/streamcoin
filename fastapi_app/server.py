from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from typing import List
#from fastapi_app.db import read_all_items, update_item, get_top5_cryptos
from db import read_all_items, update_item, get_top5_cryptos, insert_history # Importer la fonction depuis db.py
import httpx
import json

# Créer une instance de l'application FastAPI
app = FastAPI(
    title="FastAPI Starter",
    description="Un point de départ pour une application FastAPI",
    version="1.0.0",
)

# Modèle Pydantic pour les requêtes/réponses
class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cryptoid: int
    cryptoname: str
    coingeckoid: str
    alert1: float 
    alert2: float 
    alert3: float 
    alert4: float
    alert5: float
    lastprice: float 
    amount: float 
    total: float 

# Route d'accueil
@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API FastAPI Starter avec PostgreSQL!"}

# Route pour récupérer tous les items
@app.get("/items")
async def get_all_items_route():
    items = read_all_items()
    return {
        "cryptos": items
    }

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

# Route Update prices
@app.get("/updateprices")
async def update_prices_route():
    """
    Route pour mettre à jour les prix des cryptomonnaies.
    """
    # Appeler la fonction read_all_items pour récupérer les items
    items = read_all_items()

    # Trace console pour afficher les items récupérés
    print("=== Items Récupérés ===")
    print(items)
    data = json.loads(items)

    # Extraire les valeurs de 'coingeckoid' depuis les items
    cryptos = [item["coingeckoid"] for item in data]
    # Trace console pour afficher les cryptos extraites
    print("=== Cryptos ===")
    print(cryptos)

    # Appeler la fonction get_crypto_prices avec la liste des cryptomonnaies
    crypto_prices = await get_crypto_prices(cryptos)
    # Trace console pour afficher crypto_prices
    print("=== Crypto Prices ===")
    #print(crypto_prices)

    # Initialiser la somme totale
    crypto_total = float(0)

    # Parcourir les items et effectuer les calculs
    for item in data:
        # Récupérer le prix USD depuis l'API CoinGecko
        price_usd = crypto_prices.get(item["coingeckoid"], {}).get("usd", 0)
        price_usd = crypto_prices.get(item["coingeckoid"], {}).get("usd", 0)

        # Calculer la valeur totale (amount * usd)
        total = float(item["amount"]) * float(price_usd) if item["amount"] else 0
        # Ajouter au total global
        crypto_total += float(total)

        # Mettre à jour la valeur lastprice dans la base de données
        update_item(int(item["cryptoid"]), **{"lastprice": price_usd})
        update_item(int(item["cryptoid"]), **{"total": total})

    print("=== Fin de la boucle ===")
    print(f"Total des cryptos : {crypto_total}")

    insert_history(crypto_total)

    # Retourner les items et les prix des cryptomonnaies
    return {
        "crypto_prices": crypto_prices,
        "cryptototal": crypto_total
    }

# Route alertes
@app.get("/alerts")
async def alerts_route():
    """
    Route pour vérifier les alertes des cryptomonnaies.
    """
    # Appeler la fonction read_all_items pour récupérer les items
    items = read_all_items()

    # Trace console pour afficher les items récupérés
    print("=== Items Récupérés ===")
    print(items)
    data = json.loads(items)

    # Initialiser une liste pour stocker les alertes
    alerts = []

    # Liste des niveaux d'alerte du plus élevé au plus bas
    alert_levels = [("alert5", 5), ("alert4", 4), ("alert3", 3), ("alert2", 2), ("alert1", 1)]

    for item in data:  # cryptos est ta liste de données
        for alert_key, level in alert_levels:
            if item.get(alert_key) and item["lastprice"] >= item[alert_key]:
                alerts.append(
                    f"Crypto {item['cryptoname']} a atteint l'alerte {level} avec un prix de {item['lastprice']} USD"
                )
                break  # On arrête dès qu'une alerte est déclenchée
            
    print("=== Fin de la boucle ===")
    print(f"Alertes générées : {alerts}")

    # Retourner les items et les prix des cryptomonnaies
    return {
        "alerts": alerts
    }


# Route Top5   
@app.get("/top5")
async def top5_route():
    """
    Route pour récupérer le Top 5 des cryptomonnaies par total décroissant.
    """
    top5 = get_top5_cryptos()
    return {
        "top5": top5
    }

# Route pour récupérer le total des cryptomonnaies
@app.get("/total") 
async def total_route():
    """
    Route pour récupérer le total des cryptomonnaies.
    """
    from db import get_total_crypto  # Importer la fonction depuis db.py
    total = get_total_crypto()
    return {
        "cryptototal": total
    }

@app.get("/main")
async def main_route():
    """
    Route principale pour récupérer le Top 5, les alertes et le total des cryptomonnaies.
    """
    from db import get_total_crypto  # Importer la fonction depuis db.py

    top5 = get_top5_cryptos()
    total = get_total_crypto()

    # Appeler la fonction read_all_items pour récupérer les items
    items = read_all_items()
    data = json.loads(items)

    # Initialiser une liste pour stocker les alertes
    alerts = []

    # Parcourir les items et effectuer les calculs
    # for item in data:
         # Comparer le prix avec les alertes
        # if item["alert5"] and item["lastprice"] >= item["alert5"]:
        #     alerts.append(f"Crypto {item['cryptoname']} a atteint l'alerte 3 avec un prix de {item['lastprice']} USD")
        # elif item["alert4"] and item["lastprice"] >= item["alert4"]:
        #     alerts.append(f"Crypto {item['cryptoname']} a atteint l'alerte 3 avec un prix de {item['lastprice']} USD")
        # elif item["alert3"] and item["lastprice"] >= item["alert3"]:
        #     alerts.append(f"Crypto {item['cryptoname']} a atteint l'alerte 3 avec un prix de {item['lastprice']} USD")
        # elif item["alert2"] and item["lastprice"] >= item["alert2"]:
        #     alerts.append(f"Crypto {item['cryptoname']} a atteint l'alerte 2 avec un prix de {item['lastprice']} USD")
        # elif item["alert1"] and item["lastprice"] >= item["alert1"]:
        #     alerts.append(f"Crypto {item['cryptoname']} a atteint l'alerte 1 avec un prix de {item['lastprice']} USD")

    # Liste des niveaux d'alerte du plus élevé au plus bas
    alert_levels = [("alert5", 5), ("alert4", 4), ("alert3", 3), ("alert2", 2), ("alert1", 1)]

    for item in data:  # cryptos est ta liste de données
        for alert_key, level in alert_levels:
            if item.get(alert_key) and item["lastprice"] >= item[alert_key]:
                alerts.append(
                    f"Crypto {item['cryptoname']} a atteint l'alerte {level} avec un prix de {item['lastprice']} USD"
                )
                break  # On arrête dès qu'une alerte est déclenchée

    return {
        "datas": {
            "top5": top5,
            "alerts": alerts,
            "cryptototal": total
        }
    }