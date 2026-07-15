import streamlit as st
from datetime import date

def render():
    st.title("Datos de Hospitalización y Egreso")

    # --- INFORMACIÓN DE INGRESO ---
    st.subheader("1. Información de Ingreso")
    c1, c2 = st.columns(2)
    with c1:
        tipo_ingreso = st.selectbox("Tipo de ingreso", ["Primera vez", "Reingreso"], index=None)
        tipo_servicio = st.selectbox("Tipo de servicio", ["Hospitalización", "Ambulatorio"], index=None)
        cama = st.text_input("Nº de Cama")
    with c2:
        diagnostico_ingreso = st.text_area("Diagnóstico principal de ingreso")
        servicio_iaas = st.selectbox("Servicio donde adquirió la IAAS", [
            "Cardiología", "Cirugía Cardiovascular", "Cirugía de Tórax", "Cirugía Oncológica",
            "Cirugía Plástica y Reconstructiva", "Dermatología", "Endocrinología", "Gastroenterología",
            "Genética Médica", "Hematología", "Infectología", "Medicina Interna", "Nefrología",
            "Neumología", "Neurocirugía", "Neurología", "Oftalmología", "Oncología Médica",
            "Ortopedia y Traumatología", "Otorrinolaringología", "Proctología", "Reumatología",
            "Trasplante de Órganos", "Unidad de Cuidados Intensivos (UCI)", "Urología"
        ], index=None)

    # --- CRONOLOGÍA DE FECHAS ---
    st.subheader("2. Cronología de Fechas")
    f1, f2, f3 = st.columns(3)
    with f1:
        f_ingreso_hosp = st.date_input("Ingreso Hospitalario", value=None)
        f_ingreso_serv = st.date_input("Ingreso al servicio (IAAS)", value=None)
    with f2:
        f_inicio_sintomas = st.date_input("Inicio de síntomas IAAS", value=None)
        f_deteccion = st.date_input("Detección de la IAAS", value=None)
    with f3:
        f_resolucion = st.date_input("Resolución de la IAAS", value=None)
        f_egreso_hosp = st.date_input("Egreso Hospitalario", value=None)

    # --- INFORMACIÓN DE EGRESO (Condicional) ---
    if f_egreso_hosp:
        st.subheader("3. Información de Egreso")
        motivo_egreso = st.selectbox("Motivo de egreso", [
            "Perdida de vigencia", "Mejoria", "Alta voluntaria", 
            "Referencia a otro hospital", "Defunción", "Abandono no autorizado"
        ], index=None)

        if motivo_egreso == "Defunción":
            st.warning("⚠️ Registro de Defunción")
            c_def1, c_def2 = st.columns(2)
            with c_def1:
                f_defuncion = st.date_input("Fecha de defunción")
                folio_def = st.text_input("Folio de certificado de defunción")
            with c_def2:
                causa_muerte = st.radio("Causa de muerte", ["Por IAAS", "Con IAAS", "Por otra causa"])
                if causa_muerte == "Por otra causa":
                    otra_causa = st.selectbox("Seleccione otra causa", ["Falla orgánica", "Enfermedad de base", "Traumatismo", "Otro"])

    # --- ACCIÓN ---
    if st.button("Guardar registro y continuar"):
        st.session_state.datos_hospitalizacion = {
            "Tipo_Ingreso": tipo_ingreso,
            "Tipo_Servicio": tipo_servicio,
            "Cama": cama,
            "Diagnostico_Ingreso": diagnostico_ingreso,
            "Servicio_IAAS": servicio_iaas,
            "Fecha_Egreso": str(f_egreso_hosp) if f_egreso_hosp else None
        }
        st.success("Datos de hospitalización guardados correctamente.")
