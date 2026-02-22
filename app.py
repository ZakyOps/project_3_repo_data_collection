import streamlit as st

st.set_page_config(
    page_title="Coinafrique Scraper App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI improvement
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Hero Section
st.title("Projet 3 : Collecte et Analyse de Données Coinafrique")
st.markdown("---")

st.markdown("""
<div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px;'>
    <h3 style='color: #2c3e50; margin-top: 0;'>Bienvenue sur votre espace de travail</h3>
    <p style='color: #34495e; font-size: 16px;'>
        Cette application centralise toutes les étapes de votre pipeline de données : de l'extraction multi-pages sur Coinafrique jusqu'à la visualisation interactive, en passant par le nettoyage automatisé et le stockage SQL.
    </p>
</div>
""", unsafe_allow_html=True)

st.subheader("Explorez les fonctionnalités")

col1, col2 = st.columns(2)

with col1:
    st.info("### 1. Web Scraper Actif\nLancez des requêtes dynamiques pour extraire les dernières annonces en temps réel. Les résultats sont immédiatement stockés dans votre base de données locale.")
    
    st.success("### 3. Dashboard Analytique\nVisualisez les tendances du marché, les prix moyens et la répartition des catégories grâce à un nettoyage des données en arrière-plan et des graphiques interactifs Plotly.")

with col2:
    st.warning("### 2. Téléchargement Brut\nAccédez aux jeux de données extraits via l'extension Chrome Web Scraper, garantissant un accès aux données brutes non altérées pour vos propres pipelines.")
    
    st.error("### 4. Évaluation\nFaites-nous vos retours ! Un formulaire intégré vous permet d'évaluer la qualité de l'interface et des données produites.")

st.markdown("---")
st.caption("Navigation : Utilisez le menu latéral à gauche pour accéder aux différentes pages de l'application.")
