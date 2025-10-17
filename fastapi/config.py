import psycopg2

# Récupérer les informations de connexion depuis les variables d'environnement
DB_HOST = "localhost"
DB_NAME = "crypto"
DB_USER = "api"
DB_PASSWORD = "$8{(6oPd{0@+><UXZ3eg"
DB_PORT = "5032"

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
    