import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Download Raw Data", layout="wide")

st.title("Téléchargement : Données Brutes")

st.markdown("""
Récupérez ici l'ensemble des données extraites à la source via l'extension **Web Scraper**.
Ces données sont fournies telles quelles (*brutes*), sans aucun post-traitement, idéales pour construire vos propres pipelines de nettoyage.
""")
st.markdown("---")

data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'coinafrique_animaux.csv')

try:
    df_raw = pd.read_csv(data_path)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("Consulter un extrait des données brutes", expanded=True):
            st.dataframe(df_raw, use_container_width=True)
            
    with col2:
        st.info("### Métriques du fichier")
        st.metric("Nombre total de lignes", len(df_raw))
        st.metric("Nombre de colonnes", len(df_raw.columns))
        
        st.write("### Exporter")
        csv = df_raw.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger le dataset (.csv)",
            data=csv,
            file_name='coinafrique_raw_webscraper.csv',
            mime='text/csv',
            use_container_width=True,
            type="primary"
        )
except FileNotFoundError:
    st.error(f"Le fichier de données brutes est introuvable au chemin : {data_path}")
    st.info("Veuillez vous assurer que le fichier `raw_webscraper_data.csv` est présent dans le dossier `data/`.")
