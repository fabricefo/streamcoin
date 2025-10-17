import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import json

# Importer la fonction get_connection depuis config.py
from config import get_connection
       

# Fonction pour lire tous les éléments
def read_all_items():
    query = "SELECT * FROM portfolio"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return json.dumps(rows, indent=4, default=str)

# Fonction pour mettre à jour un élément
def update_item(cryptoid, **kwargs):
    set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
    values = list(kwargs.values())  + [cryptoid]

    query = sql.SQL("UPDATE portfolio SET {} WHERE cryptoid = %s").format(
        sql.SQL(set_clause)
    )

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
            return cur.rowcount

# Tester la fonction read_all_items
if __name__ == "__main__":
    items = read_all_items()
    print("Items récupérés depuis la base de données :")
    for item in items:
        print(item)
