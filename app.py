import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Configuration de la page Streamlit
st.set_page_config(page_title="Générateur de Clé & Grille de Correction", layout="wide")

st.title("📐 Concepteur de Clé et Grille de Correction (Maths Bénin - APC)")
st.write("Téléversez vos documents ci-dessous pour générer la clé et la grille de correction.")

# Configuration de la clé API dans le menu latéral
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Clé API Gemini", type="password")

# Fonction d'extraction du texte PDF
def lire_pdf(fichier):
    lecteur = PdfReader(fichier)
    texte = ""
    for page in lecteur.pages:
        texte += page.extract_text() or ""
    return texte

# Zones de téléchargement des documents
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Guide pédagogique")
    guide_file = st.file_uploader("Guide de la classe (PDF)", type=["pdf"])

with col2:
    st.subheader("2. Exemple de clé")
    example_file = st.file_uploader("Exemple de clé/grille (PDF)", type=["pdf"])

with col3:
    st.subheader("3. Épreuve à corriger")
    exam_file = st.file_uploader("Épreuve de maths (PDF)", type=["pdf"])

# Traitement IA
if st.button("🚀 Générer la clé et la grille de correction"):
    if not api_key:
        st.error("Veuillez saisir votre clé API Gemini dans le menu latéral à gauche.")
    elif not (guide_file and example_file and exam_file):
        st.warning("Veuillez importer l'ensemble des 3 fichiers PDF requis.")
    else:
        with st.spinner("Analyse des documents et génération de la clé de correction..."):
            try:
                texte_guide = lire_pdf(guide_file)
                texte_exemple = lire_pdf(example_file)
                texte_epreuve = lire_pdf(exam_file)

                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")

                prompt = f"""
                Tu es un expert pédagogique en mathématiques au Bénin (Approche Par Compétences - APC).
                
                Voici les éléments de référence :
                
                --- GUIDE PÉDAGOGIQUE ---
                {texte_guide[:4000]}
                
                --- MODÈLE DE CLÉ ET GRILLE PRÉCÉDENT ---
                {texte_exemple[:4000]}
                
                --- ÉPREUVE À CORRIGER ---
                {texte_epreuve}
                
                Consigne :
                Rédige la clé de correction détaillée et la grille d'évaluation (Critères Minimaux CM1, CM2, CM3 et Critères de Perfectionnement CP) strictement adaptées à l'épreuve fournie, en respectant la structure du modèle exemple et les directives du guide pédagogique.
                """

                response = model.generate_content(prompt)

                st.success("Génération terminée !")
                st.markdown("### Résultat :")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Une erreur est survenue lors de la génération : {e}")
