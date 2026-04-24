import streamlit as st 
import pandas as pd 
import numpy as np 

# --- 1. Configuration & Design --- 
st.set_page_config(page_title="Agri-Collecte Pro - Wals", page_icon="🌿", layout="centered") 

# Initialisation des variables de session
if 'historique' not in st.session_state: 
    st.session_state.historique = [] 

if 'inscrit' not in st.session_state:
    st.session_state.inscrit = False

# Style CSS pour l'interface Multicolore et Design Vert
st.markdown(""" 
    <style> 
    .stApp { background-color: #f1f8e9; } 
    
    .inscription-header {
        background: linear-gradient(to right, #ff5f6d, #ffc371, #48c6ef, #6f86d6, #2e7d32);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    .main-header { 
        background-color: #2e7d32; padding: 20px; border-radius: 15px; 
        color: white; text-align: center; margin-bottom: 25px; 
        border-bottom: 5px solid #1b5e20; 
    } 
    </style> 
    """, unsafe_allow_html=True) 

# --- 2. LOGIQUE D'INTERFACE : INSCRIPTION OU RECENSEMENT ---
if not st.session_state.inscrit:
    st.markdown("""
        <div class="inscription-header">
            <h1>📝 CRÉER VOTRE PROFIL</h1>
            <p>Bienvenue sur Agri-Collecte Pro</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("form_inscription"):
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            nom_user = st.text_input("👤 Nom et Prénom")
            
            # Champ texte pour le téléphone
            tel_input = st.text_input("📞 Numéro de téléphone", help="Chiffres uniquement")
            
        with col_in2:
            email_user = st.text_input("📧 Adresse Email (Facultatif)")
            st.info("💡 Le système rejettera toute lettre après validation.")

        valider_inscription = st.form_submit_button("🚀 S'inscrire et Accéder")
        
        if valider_inscription:
            # Vérification : est-ce que ce sont uniquement des chiffres ?
            if nom_user and tel_input:
                if tel_input.isdigit(): # <--- C'est ici que le blocage se fait
                    st.session_state.inscrit = True
                    st.session_state.nom_profil = nom_user
                    st.session_state.tel_profil = tel_input
                    st.rerun()
                else:
                    st.error("❌ Erreur : Le numéro de téléphone ne doit contenir que des chiffres (pas de lettres, pas d'espaces).")
            else:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires.")

else:
    st.markdown(f""" 
        <div class="main-header"> 
            <h1>🌿 AGRI-COLLECTE & DIAGNOSTIC</h1> 
            <p>Connecté en tant que : <b>{st.session_state.nom_profil}</b></p> 
        </div> 
        """, unsafe_allow_html=True) 
    
    if st.sidebar.button("🔌 Se déconnecter"):
        st.session_state.inscrit = False
        st.rerun()

    st.subheader("📝 Fiche de Recensement") 
    col1, col2 = st.columns(2) 

    with col1: 
        nom = st.text_input("👤 Nom de l'exploitant") 
        
        # Sélection de la culture
        liste_cultures = ["Maïs", "Manioc", "Cacao", "Café", "Banane", "Autre"] 
        choix = st.selectbox("🌱 Type de culture", liste_cultures) 
        
        # Logique pour "Autre"
        if choix == "Autre": 
            culture = st.text_input("👉 Saisissez le nom de votre culture", placeholder="Ex: Ananas, Soja...") 
        else: 
            culture = choix 
        
        etat = st.select_slider( 
            "🌡️ État de la culture", 
            options=["Attaque d'insectes", "Sécheresse", "Carence", "Moyen", "Bon", "Excellent"], 
            value="Bon" 
        ) 

    with col2: 
        u_surf = st.radio("📏 Unité de surface", ["Hectares", "Quarts"], horizontal=True) 
        val_surf = st.number_input(f"Surface ({u_surf})", min_value=0.1, step=0.25) 
        surf_ha = val_surf / 4 if u_surf == "Quarts" else val_surf 
        
        unite_qte = st.selectbox("Unité de récolte", ["Kilogrammes (kg)", "Sacs (50kg)", "Sacs (100kg)", "Tonnes (t)"]) 
        val_qte = st.number_input("Quantité récoltée", min_value=0.0) 

        dict_conv = {"Kilogrammes (kg)": 0.001, "Sacs (50kg)": 0.05, "Sacs (100kg)": 0.1, "Tonnes (t)": 1.0} 
        qte_tonnes = val_qte * dict_conv[unite_qte] 

    # Analyse et graphiques
    if surf_ha > 0 and qte_tonnes > 0: 
        rendement = qte_tonnes / surf_ha 
        st.write("---") 
        st.subheader(f"🔍 Analyse & Diagnostic : {culture}") 
        
        col_res1, col_res2 = st.columns(2) 
        col_res1.metric("Rendement", f"{rendement:.2f} T/Ha") 

        with col_res2: 
            st.write("**🩺 Critiques & Conseils :**") 
            if etat == "Attaque d'insectes": 
                st.error("🚨 **ALERTE :** Présence de nuisibles.") 
            elif etat == "Sécheresse": 
                st.warning("⚠️ **ALERTE :** Stress hydrique.") 
            elif etat == "Carence": 
                st.info("🧪 **CONSEIL :** Apport en engrais nécessaire.") 
            
            if rendement < 1.0: 
                st.error("📉 **Rendement Critique**") 
            elif rendement >= 3.0: 
                st.success("🌟 **Rendement Top**") 

        st.write("### 📈 Courbe de variation du rendement") 
        annees = [2023, 2024, 2025, 2026] 
        valeurs_courbe = [rendement * 0.8, rendement * 1.1, rendement * 0.95, rendement] 
        df_chart = pd.DataFrame({"Année": annees, "Rendement (T/Ha)": valeurs_courbe}) 
        st.line_chart(df_chart.set_index("Année")) 

    st.write("---") 
    if st.button("🚀 Valider et Enregistrer dans l'Historique"): 
        # CRUCIAL : On vérifie que 'culture' n'est pas vide (surtout si 'Autre' est choisi)
        if nom and culture: 
            nouvelle_entree = { 
                "Exploitant": nom, 
                "Culture": culture, # Enregistre la valeur saisie manuellement ou le choix
                "Surface (Ha)": round(surf_ha, 2), 
                "Récolte (T)": round(qte_tonnes, 2), 
                "Rendement (T/Ha)": round(qte_tonnes/surf_ha, 2), 
                "État": etat 
            } 
            st.session_state.historique.append(nouvelle_entree) 
            st.balloons() 
            st.success(f"Recensement de {nom} pour la culture de {culture} enregistré !") 
        else:
            st.warning("⚠️ Veuillez remplir le nom de l'exploitant et le type de culture.")

    st.subheader("📋 Historique des Enregistrements") 
    if st.session_state.historique: 
        df_histo = pd.DataFrame(st.session_state.historique) 
        st.dataframe(df_histo, use_container_width=True) 
        
        if st.button("🗑️ Effacer tout l'historique"): 
            st.session_state.historique = [] 
            st.rerun() 
    else: 
        st.info("Aucun recensement enregistré pour le moment.")
