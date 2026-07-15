import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

def render():
    st.title("Identificación del Paciente")
    
    # Listas (mismas que tenías)
    estados = ["Aguascalientes", "Baja California", "Ciudad de México", "Puebla", "Yucatán", "Zacatecas"]
    paises = sorted(["Alemania", "Argentina", "Belice", "Bolivia", "Brasil", "Canadá", "Chile", "Colombia", "México", "Venezuela"])

    # 1. PREGUNTA FUERA DEL FORMULARIO para que el cambio sea inmediato
    st.subheader("Información Migratoria")
    es_migrante = st.radio("¿El paciente es migrante?", ["No", "Sí"], index=0)

    # 2. INICIO DEL FORMULARIO
    with st.form("form_paciente"):
        st.subheader("Datos Generales")
        # ... (Tus otros campos: expediente, nombres, etc.) ...
        
        # 3. LÓGICA DE MIGRANTE DENTRO DEL FORMULARIO
        # Como es_migrante está fuera, el formulario lo "lee" correctamente al renderizar
        if es_migrante == "Sí":
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                nac = st.selectbox("País de nacionalidad", paises, index=None, placeholder="Seleccione...")
                orig = st.selectbox("País de origen", paises, index=None, placeholder="Seleccione...")
            with c_m2:
                st.write("Países en tránsito:")
                t1 = st.selectbox("1", paises, index=None, label_visibility="collapsed")
                # ... (resto de tus selects)
            
            hosp = st.radio("¿Durante su tránsito estuvo hospitalizado?", ["No", "Sí"])
            if hosp == "Sí":
                pais_hosp = st.selectbox("¿En qué país estuvo hospitalizado?", paises, index=None)

        submit = st.form_submit_button("Guardar Paciente y Continuar")

        if submit:
            st.session_state.datos_paciente = {
                "Es_Migrante": es_migrante,
                # ... resto de tus datos
            }
            st.success("Información guardada.")
