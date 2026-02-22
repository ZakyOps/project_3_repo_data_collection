import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Tableau de bord Analytique")
st.markdown("Plongez dans l'analyse de nos données extraites. Le tableau de bord nettoie automatiquement les prix pour identifier les tendances du marché.")

@st.cache_data
def load_and_clean_data(file_path):
    if not os.path.exists(file_path):
        return None
        
    df = pd.read_csv(file_path)
    
    cols_to_drop = ['web-scraper-order', 'web-scraper-start-url']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
    
    def get_cat(row):
        val = str(row.get('V1_Nom_ou_details', '')).lower()
        if 'chien' in val: return 'Chiens'
        if 'mouton' in val: return 'Moutons'
        if 'poule' in val or 'lapin' in val or 'pigeon' in val: return 'Poules, Lapins, Pigeons'
        return 'Autres Animaux'
        
    df['Categorie'] = df.apply(get_cat, axis=1)
    
    df['Prix_Num'] = df['V2_prix'].astype(str).str.replace('CFA', '', regex=False)
    df['Prix_Num'] = df['Prix_Num'].str.replace(' ', '', regex=False)
    df['Prix_Num'] = pd.to_numeric(df['Prix_Num'], errors='coerce')
    
    df = df.fillna('N/A')
    
    return df

data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw_webscraper_data.csv')
df_clean = load_and_clean_data(data_path)

if df_clean is not None:
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'coinafrique_app.db')
    try:
        conn = sqlite3.connect(db_path)
        df_clean.astype(str).to_sql('Animaux_Cleaned', conn, if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        st.error(f"Erreur SQL : {e}")
        
    # --- KPIs Row ---
    st.markdown("### Indicateurs Clés")
    kpi1, kpi2, kpi3 = st.columns(3)
    
    total_annonces = len(df_clean)
    prix_moyen_global = df_clean['Prix_Num'].mean()
    nb_categories = df_clean['Categorie'].nunique()
    
    kpi1.metric("Total Annonces", f"{total_annonces}")
    kpi2.metric("Prix Moyen Global", f"{prix_moyen_global:,.0f} CFA" if pd.notnull(prix_moyen_global) else "N/A")
    kpi3.metric("Catégories Actives", f"{nb_categories}")
    
    st.markdown("---")
    
    # --- Visualizations ---
    tab_graphs, tab_data = st.tabs(["Visualisations", "Données Nettoyées"])
    
    with tab_graphs:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Répartition du Volume")
            cat_counts = df_clean['Categorie'].value_counts().reset_index()
            cat_counts.columns = ['Categorie', 'Nombre']
            fig1 = px.pie(cat_counts, names='Categorie', values='Nombre', hole=0.4, 
                          color_discrete_sequence=px.colors.sequential.RdBu)
            fig1.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            st.subheader("Prix Moyen Estimé (CFA)")
            df_prices = df_clean[pd.to_numeric(df_clean['Prix_Num'], errors='coerce').notnull()]
            mean_prices = df_prices.groupby('Categorie')['Prix_Num'].mean().reset_index()
            fig2 = px.bar(mean_prices, x='Categorie', y='Prix_Num', text_auto='.0f', 
                          color='Categorie', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig2.update_layout(showlegend=False, xaxis_title="", yaxis_title="")
            st.plotly_chart(fig2, use_container_width=True)
            
    with tab_data:
        st.subheader("Jeu de données après traitement")
        st.dataframe(df_clean, use_container_width=True)
        
else:
    st.warning("Aucune donnée brute trouvée pour générer ce tableau de bord.")
