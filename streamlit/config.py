import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()


# Récupérer les informations de connexion depuis les variables d'environnement
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_NAME = os.getenv("DB_NAME", "test")
# DB_USER = os.getenv("DB_USER", "test")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
# DB_PORT = os.getenv("DB_PORT", "5432")

DB_HOST = "postgres"
DB_NAME = "crypto"
DB_USER = "api"
DB_PASSWORD = "$8{(6oPd{0@+><UXZ3eg"
DB_PORT = "5432"

# URL de connexion pour SQLAlchemy
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configuration de SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Fonction pour se connecter à PostgreSQL
def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        return conn
    except Exception as e:
        raise Exception(f"Erreur de connexion à la base de données : {e}")
    
# Fonction pour obtenir une session de base de données avec SQLAlchemy
async def get_db():
    async with SessionLocal() as session:
        yield session