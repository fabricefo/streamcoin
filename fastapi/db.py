import psycopg2
from psycopg2.extras import sql

# Importer la fonction get_connection depuis config.py
from config import get_connection

        

# Fonction pour lire tous les éléments
def read_all_items():
    query = "SELECT * FROM portfolio"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            items = []
            for row in rows:
                item = {
                    "cryptoid": row[0],
                    "cryptoname": row[1],
                    "coingeckoid": row[2],
                    "alert1": row[3],
                    "alert2": row[4],
                    "alert3": row[5],
                    "lastprice": row[6],
                    "amount": row[7],
                    "total": row[8],
                }
                items.append(item)
            return items

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
