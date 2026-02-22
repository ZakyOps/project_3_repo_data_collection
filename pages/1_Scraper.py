import streamlit as st
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import os

st.set_page_config(page_title="Scraper", layout="wide")

# CSS and styling
st.markdown("""
<style>
    .reportview-container {
        margin-top: -2em;
    }
    .stProgress .st-bo {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

st.title("Scraper Actif : Coinafrique")
st.markdown("Extrayez en temps réel des données depuis Coinafrique grâce à notre moteur de scraping basé sur `BeautifulSoup` et `Requests`.")

categories = {
    "Chiens": "https://sn.coinafrique.com/categorie/chiens",
    "Moutons": "https://sn.coinafrique.com/categorie/moutons",
    "Poules, Lapins, Pigeons": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
    "Autres Animaux": "https://sn.coinafrique.com/categorie/autres-animaux"
}

# --- Sidebar settings ---
with st.sidebar:
    st.header("Paramètres")
    category_choice = st.selectbox("Catégorie cible :", list(categories.keys()))
    num_pages = st.number_input("Pages à scraper :", min_value=1, max_value=50, value=1, help="Attention, un nombre élevé peut prendre plus de temps.")
    start_btn = st.button("Lancer l'extraction", use_container_width=True)

# --- Layout main area ---
col_info, col_results = st.columns([1, 2])

with col_info:
    st.info("**Comment ça marche ?**\nSélectionnez vos paramètres dans la barre latérale. Le système ira lire le code HTML des pages demandées, en extraira les informations clés (Prix, Adresse, etc.) et les stockera automatiquement dans votre base de données locale sécurisée.")

if start_btn:
    st.markdown("---")
    url_base = categories[category_choice]
    data = []
    
    st.write(f"### Scraping en cours : {category_choice}")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    start_time = time.time()
    
    for i in range(1, num_pages + 1):
        status_text.text(f"Récupération de la page {i}/{num_pages}...")
        url = f"{url_base}?page={i}"
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            containers = soup.find_all('div', class_='col s6 m4 l3')
            
            for container in containers:
                try:
                    nom_tag = container.select_one('p.ad__card-description')
                    v1 = nom_tag.text.strip() if nom_tag else None
                    
                    price_tag = container.select_one('.ad__card-price')
                    v2 = price_tag.text.strip().replace('CFA', '').replace(' ', '') if price_tag else None
                    
                    adr_tag = container.select_one("p.ad__card-location > span")
                    v3 = adr_tag.text.strip() if adr_tag else None
                    
                    img_tag = container.select_one(".card-image img")
                    v4 = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
                    
                    data.append({
                        "V1_Nom_ou_details": v1,
                        "V2_prix": v2,
                        "V3_adresse": v3,
                        "V4_image_lien": v4,
                        "Categorie": category_choice
                    })
                except Exception:
                    continue
        except Exception as e:
            st.error(f"Erreur réseau sur la page {i}: {e}")
            
        progress_bar.progress(i / num_pages)
        time.sleep(0.5)
        
    end_time = time.time()
    status_text.text("Extraction terminée !")
    
    if data:
        df = pd.DataFrame(data)
        
        # Display Metrics
        met1, met2, met3 = st.columns(3)
        met1.metric("Annonces extraites", f"{len(df)}")
        met2.metric("Catégorie", category_choice)
        met3.metric("Temps d'exécution", f"{end_time - start_time:.1f} s")
        
        st.success("Extraction réussie avec succès.")
        
        with st.expander("Aperçu des données extraites", expanded=True):
            st.dataframe(df, use_container_width=True)
        
        # Save to SQLite
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'coinafrique_app.db')
            conn = sqlite3.connect(db_path)
            df.to_sql('Animaux_Scraped', conn, if_exists='append', index=False)
            conn.close()
            st.toast("Données sauvegardées dans `Animaux_Scraped` via SQLite.")
        except Exception as e:
            st.error(f"Erreur de base de données : {e}")
    else:
        st.warning("Aucune donnée n'a pu être extraite. Le site a peut-être changé sa structure.")
