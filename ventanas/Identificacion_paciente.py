import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

def render():
    st.title("Identificación del Paciente")
    
    estados = ["Aguascalientes", "Baja California", "Ciudad de México", "Puebla", "Yucatán", "Zacatecas"]
    paises = sorted(["Alemania", "Argentina", "Belice", "Bolivia", "Brasil", "Canadá", "Chile", "Colombia", "México", "Venezuela"])

    # Usamos un form para los datos generales
    with st.form("form_paciente"):
        st.subheader("Datos Generales")
        expediente = st.text_input("Nº de expediente", placeholder="Ej. 123456")
        
        c1, c2, c3 = st.columns(3)
        with c1: ap_paterno = st.text_input("Apellido Paterno")
        with c2: ap_materno = st.text_input("Apellido Materno")
        with c3: nombres = st.text_input("Nombres")

        c_fec, c_ed = st.columns(2)
        with c_fec:
            f_nacimiento = st.date_input("Fecha de nacimiento", value=None, min_value=date(1900, 1, 1))
        with c_ed:
            edad_str = ""
            if f_nacimiento:
                delta = relativedelta(date.today(), f_nacimiento)
                edad_str = f"{delta.years} Años, {delta.months} Meses, {delta.days} Días"
            st.text_input("Edad", value=edad_str, disabled=True, placeholder="Se calcula automáticamente")

        # --- LÓGICA DE MIGRANTE ---
        st.subheader("Información Migratoria")
        
        # El on_change=st.rerun es la CLAVE para que al dar clic en "Sí" aparezca el menú
        es_migrante = st.radio("¿El paciente es migrante?", ["No", "Sí"], 
                               index=0 if 'migrante_choice' not in st.session_state or st.session_state.migrante_choice == "No" else 1,
                               key="migrante_choice", on_change=st.rerun)

        if st.session_state.migrante_choice == "Sí":
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                nac = st.selectbox("País de nacionalidad", paises, index=None, placeholder="Seleccione...")
                orig = st.selectbox("País de origen", paises, index=None, placeholder="Seleccione...")
            with c_m2:
                st.markdown("**Países en tránsito:**")
                t1 = st.selectbox("Tránsito 1", paises, index=None, placeholder="Seleccione...")
                t2 = st.selectbox("Tránsito 2", paises, index=None, placeholder="Seleccione...")
                t3 = st.selectbox("Tránsito 3", paises, index=None, placeholder="Seleccione...")
                t4 = st.selectbox("Tránsito 4", paises, index=None, placeholder="Seleccione...")
            
            viaje = st.radio("¿Ha viajado a otro país durante los últimos 3 meses?", ["No", "Sí"])
            hosp = st.radio("¿Durante su tránsito estuvo hospitalizado?", ["No", "Sí"])
            
            if hosp == "Sí":
                pais_hosp = st.selectbox("¿En qué país estuvo hospitalizado?", paises, index=None, placeholder="Seleccione país...")

        # Botón de Guardado al final
        submit = st.form_submit_button("Guardar registro y continuar")

        if submit:
            if not f_nacimiento:
                st.error("Por favor, ingresa la fecha de nacimiento.")
            else:
                st.session_state.datos_paciente = {
                    "Nombre": f"{nombres} {ap_paterno}",
                    "Es_Migrante": st.session_state.migrante_choice
                }
                st.success("Registro guardado exitosamente.")
