import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importer la fonction get_connection depuis config.py
from config import get_connection

# Configuration de la page
st.set_page_config(
    page_title="Application Streamlit de Départ",
    page_icon="📊",
    layout="wide",
)

# Sidebar
st.sidebar.title("Navigation")
options = st.sidebar.radio("Aller à", ["Accueil", "Données", "Visualisation"])

# Accueil
if options == "Accueil":
    st.title("Bienvenue dans l'application Streamlit 🎉")
    st.write(
        """
        Cette application est un point de départ pour développer une application Streamlit plus complète.
        Vous pouvez naviguer entre les sections via la barre latérale.
        """
    )
    st.image(
        "https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png",
        width=300,
    )

# Données
elif options == "Données":
    st.title("Affichage des Données")
    st.write("Voici un exemple de tableau de données généré aléatoirement :")

    # Connexion à la base de données
    conn = get_connection()
    if conn:
        try:
            # Requête SQL pour récupérer des données
            query = "SELECT id, libelle, range_debut, range_fin FROM vlan LIMIT 10;"  # Remplacez par votre table et colonnes
            db_data = pd.read_sql_query(query, conn)

            # Ajouter les données SQL à la DataFrame existante
            st.write("Données récupérées depuis la base PostgreSQL :")
            st.dataframe(db_data)

        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête SQL : {e}")
        finally:
            conn.close()

    # Option de téléchargement
    st.download_button(
        label="Télécharger les données",
        data=db_data.to_csv(index=False),
        file_name="donnees.csv",
        mime="text/csv",
    )

# Visualisation
elif options == "Visualisation":
    st.title("Visualisation des Données")
    st.write("Voici un exemple de graphique simple :")

    # Générer des données pour le graphique
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Créer le graphique
    fig, ax = plt.subplots()
    ax.plot(x, y, label="sin(x)")
    ax.set_title("Graphique de sin(x)")
    ax.set_xlabel("x")
    ax.set_ylabel("sin(x)")
    ax.legend()

    # Afficher le graphique
    st.pyplot(fig)