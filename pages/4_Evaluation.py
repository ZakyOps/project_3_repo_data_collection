import streamlit as st

st.set_page_config(page_title="Evaluation")

st.title("Formulaire d'évaluation")

st.write("Merci d'avoir utilisé notre application ! Veuillez remplir le formulaire d'évaluation ci-dessous.")

st.info("L'URL par défaut ci-dessous est un modèle vide. Vous pouvez coller le lien de votre propre formulaire (Google Forms ou Kobo) dans la case.")
google_form_url = st.text_input(
    "Lien de votre formulaire :", 
    value="https://docs.google.com/forms/d/e/1FAIpQLSf4oHly6t4yIe-M_0o1EebpGg0wz869pYmKzJbbYp-XoYxIfQ/viewform?embedded=true"
)

if google_form_url:
    st.markdown(f"""
    <a href="{google_form_url}" target="_blank">
        <button style="
            background-color: #4CAF50; 
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;">
            Accéder au formulaire (Ouvrir dans un nouvel onglet)
        </button>
    </a>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.write("Ou remplissez-le directement ici :")

    # Embed the google form as an iframe
    try:
        st.components.v1.iframe(google_form_url, height=800, scrolling=True)
    except Exception as e:
        st.error(f"Le lien n'a pas pu être intégré dans la page : {e}")
