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
    
    # Nettoyage de la catégorie
    def get_cat(row):
        val_v1 = str(row.get('V1', row.get('V1_Nom_ou_details', ''))).lower()
        # On regarde aussi l'URL si V1 est vide
        val_url = str(row.get('web_scraper_start_url', '')).lower()
        combined = val_v1 + " " + val_url
        
        if 'chiens' in combined or 'chien' in combined: return 'Chiens'
        if 'moutons' in combined or 'mouton' in combined: return 'Moutons'
        if 'poules' in combined or 'lapins' in combined or 'pigeons' in combined: return 'Poules, Lapins, Pigeons'
        return 'Autres Animaux'
        
    df['Categorie'] = df.apply(get_cat, axis=1)
    
    # Nettoyage du prix : on garde NaN pour les calculs
    price_col = 'V2' if 'V2' in df.columns else 'V2_prix'
    df['Prix_Num'] = df[price_col].astype(str).str.replace('CFA', '', regex=False).str.replace(' ', '', regex=False)
    # Remplacer les virgules éventuelles par des points ou rien si c'est un séparateur de milliers
    df['Prix_Num'] = pd.to_numeric(df['Prix_Num'], errors='coerce')
    
    # Remplir les autres colonnes pour l'affichage, mais laisser Prix_Num tel quel pour le moment
    # ou remplir Prix_Num après le calcul. Préférable de garder les NaNs pour mean()
    
    return df

data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'coinafrique_animaux.csv')
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
        st.dataframe(df_clean.fillna('N/A'), use_container_width=True)
        
        # Add download button for cleaned data
        csv_clean = df_clean.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données nettoyées (.csv)",
            data=csv_clean,
            file_name='coinafrique_animaux_clean.csv',
            mime='text/csv',
            use_container_width=False,
            help="Téléchargez la version traitée avec les catégories détectées et les prix numériques."
        )
        
else:
    st.warning("Aucune donnée brute trouvée pour générer ce tableau de bord.")
