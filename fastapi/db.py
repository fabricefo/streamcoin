from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import text
from sqlalchemy import Column, Integer, String, Float, Numeric
import sys
from pathlib import Path
import asyncio

# Ajouter le répertoire parent au chemin Python
sys.path.append(str(Path(__file__).resolve().parent.parent / "config"))

# Importer la fonction get_connection depuis utils.py
from config import Base, get_db

class ItemDB(Base):
    __tablename__ = "portfolio"

    cryptoid = Column(Integer, primary_key=True, index=True)
    cryptoname = Column(String, index=True)
    coingeckoid = Column(String, index=True)
    alert1 = Column(Float, nullable=True)
    alert2 = Column(Float, nullable=True)
    alert3= Column(Float, nullable=True)
    amount = Column(Float, nullable=True)
    lastprice = Column(Float, nullable=True)
    total = Column(Float, nullable=True)
    
    def __repr__(self):
        return (
            f"<ItemDB(cryptoid={self.cryptoid}, cryptoname='{self.cryptoname}', "
            f"coingeckoid='{self.coingeckoid}', alert1={self.alert1}, alert2={self.alert2}, "
            f"alert3={self.alert3}, amount={self.amount}, lastprice={self.lastprice}, total={self.total})>"
        )
        
# Fonction pour créer un nouvel élément
async def create_item(db: AsyncSession, item_data: dict):
    new_item = ItemDB(**item_data)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

# Fonction pour lire tous les éléments
async def read_all_items(db: AsyncSession):
    query = select(ItemDB)
    result = await db.execute(query)
    return result.scalars().all()

# Fonction pour lire un élément par ID
async def read_item_by_id(db: AsyncSession, item_id: int):
    query = select(ItemDB).where(ItemDB.cryptoid == item_id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    return item

# Fonction pour mettre à jour un élément
async def update_item(db: AsyncSession, item_id: int, updated_data: dict):
    item = await read_item_by_id(db, item_id)
    if not item:
        return None
    for key, value in updated_data.items():
        setattr(item, key, value)
    await db.commit()
    await db.refresh(item)
    return item

# Fonction pour supprimer un élément
async def delete_item(db: AsyncSession, item_id: int):
    item = await read_item_by_id(db, item_id)
    if not item:
        return None
    await db.delete(item)
    await db.commit()
    return item


# Tester la fonction read_all_items
if __name__ == "__main__":
    from config import get_db  # Importer get_db pour obtenir une session de base de données

    async def test_read_all_items():

        # Obtenir une session de base de données
        async for db in get_db():
            items = await read_all_items(db)
            print("Items récupérés depuis la base de données :")
            for item in items:
                print(item)

    async def test_update_item():

        # ID de l'élément à mettre à jour
        test_item_id = 1  # Remplacez par un ID valide dans votre base de données

        # Données de mise à jour
        updated_data = {
            "lastprice": 30000.0,
            "total": 60000.0
        }

        # Obtenir une session de base de données
        async for db in get_db():
            # Lire l'élément avant la mise à jour
            print("=== Avant la mise à jour ===")
            item = await read_item_by_id(db, int(test_item_id))
            print(item)

            # Mettre à jour l'élément
            await update_item(db, int(test_item_id), updated_data)

            # Lire l'élément après la mise à jour
            print("=== Après la mise à jour ===")
            item = await read_item_by_id(db, int(test_item_id))
            print(item)

    # Exécuter le test
    # Obtenir ou créer une boucle événementielle
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Exécuter les tests
    loop.run_until_complete(test_read_all_items())
    loop.run_until_complete(test_update_item())
