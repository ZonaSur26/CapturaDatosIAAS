import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

def render():
    st.title("Identificación del Paciente")

    estados = ["Aguascalientes", "Baja California", "Ciudad de México", "Puebla", "Yucatán", "Zacatecas"]
    paises = sorted(["Alemania", "Argentina", "Belice", "Bolivia", "Brasil", "Canadá", "Chile", "Colombia", "México", "Venezuela"])

    # Datos Generales
    st.subheader("Datos Generales")
    expediente = st.text_input("Nº de expediente")
    c1, c2, c3 = st.columns(3)
    with c1: ap_paterno = st.text_input("Apellido Paterno")
    with c2: ap_materno = st.text_input("Apellido Materno")
    with c3: nombres = st.text_input("Nombres")

    c_fec, c_ed = st.columns(2)
    with c_fec:
        f_nacimiento = st.date_input("Fecha de nacimiento (dd/mm/aaaa)", value=None)
    with c_ed:
        edad_str = ""
        if f_nacimiento:
            delta = relativedelta(date.today(), f_nacimiento)
            edad_str = f"{delta.years} Años, {delta.months} Meses, {delta.days} Días"
        st.text_input("Edad", value=edad_str, disabled=True)

    # --- Lógica de Migrante (Dinámica) ---
    st.subheader("Información Migratoria")
    es_migrante = st.radio("¿El paciente es migrante?", ["No", "Sí"], index=0)

    if es_migrante == "Sí":
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            nac = st.selectbox("País de nacionalidad", paises, index=None)
            orig = st.selectbox("País de origen", paises, index=None)
        with c_m2:
            st.markdown("**Países en tránsito:**")
            t1 = st.selectbox("País 1", paises, index=None)
            t2 = st.selectbox("País 2", paises, index=None)
            t3 = st.selectbox("País 3", paises, index=None)
            t4 = st.selectbox("País 4", paises, index=None)
        
        viaje = st.radio("¿Ha viajado a otro país?", ["No", "Sí"])
        hosp = st.radio("¿Estuvo hospitalizado?", ["No", "Sí"])
        if hosp == "Sí":
            pais_hosp = st.selectbox("¿En qué país?", paises, index=None)

    st.markdown("---")
    
    # Botón al final
    if st.button("Guardar registro y continuar"):
        if not f_nacimiento:
            st.error("Por favor, ingresa la fecha de nacimiento.")
        else:
            st.session_state.datos_paciente = {
                "Expediente": expediente,
                "Nombre": f"{nombres} {ap_paterno} {ap_materno}",
                "Es_Migrante": es_migrante
            }
            st.success("Información guardada correctamente.")
