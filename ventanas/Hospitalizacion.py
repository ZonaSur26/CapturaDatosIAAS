import streamlit as st
import sys
from datetime import date
from config import ORDEN

# Función para forzar mayúsculas en tiempo real
def to_upper(key):
    st.session_state[key] = str(st.session_state[key]).upper()

def render():
    st.title("Datos de Hospitalización y Egreso")

    # --- INFORMACIÓN DE INGRESO ---
    st.subheader("1. Información de Ingreso")
    c1, c2 = st.columns(2)
    with c1:
        tipo_ingreso = st.selectbox("Tipo de ingreso", ["Primera vez", "Reingreso"], index=None, placeholder="Seleccione...")
        tipo_servicio = st.selectbox("Tipo de servicio", ["Hospitalización", "Ambulatorio"], index=None, placeholder="Seleccione...")
        cama = st.text_input("Nº de Cama", key="Cama", on_change=to_upper, args=["Cama"])
    
    with c2:
        diagnostico_ingreso = st.text_area("Diagnóstico principal de ingreso", key="Diag_Ingreso", on_change=to_upper, args=["Diag_Ingreso"])
        
        servicios_iaas = sorted(["ADMINISTRACIÓN DE QUIMIOTERAPIA AMBULATORIA", "AISLADOS", "ANESTESIOLOGÍA", "CARDIOLOGÍA", "CIRUGÍA GENERAL", "CLÍNICA DE HERIDAS Y ESTOMAS", "CONSULTA EXTERNA", "CUNERO", "DERMATOLOGÍA", "DIÁLISIS", "ENDOCRINOLOGÍA", "ENDOSCOPIA", "ESTOMATOLOGÍA", "GASTROENTEROLOGÍA", "GENÉTICA", "GERIATRÍA", "GINECOLOGÍA", "HEMATOLOGÍA", "HEMODIÁLISIS", "INFECTOLOGIA", "INHALOTERAPIA ADULTOS", "INMUNOLOGÍA", "MEDICINA INTERNA", "NEFROLOGÍA", "NEONATOLOGÍA", "NEUMOLOGÍA", "NEUROCIRUGÍA", "NEUROLOGÍA", "OBSTETRICIA", "OFTALMOLOGÍA", "ONCOLOGÍA", "ORTOPEDIA", "OTORRINOLARINGOLOGÍA", "PEDIATRÍA", "PSIQUIATRÍA", "REHABILITACIÓN", "REUMATOLOGÍA", "TERAPIA INTENSIVA ADULTO", "URGENCIAS", "UROLOGÍA"])
        servicio_iaas = st.selectbox("Servicio donde adquirió la IAAS", servicios_iaas, index=None, placeholder="Seleccione...")

    st.subheader("2. Cronología de Fechas")
    f1, f2, f3 = st.columns(3)
    with f1:
        f_ingreso_hosp = st.date_input("🏥 Ingreso Hospitalario", value=None, format="DD/MM/YYYY")
        f_ingreso_serv = st.date_input("🩺 Ingreso al servicio (IAAS)", value=None, format="DD/MM/YYYY")
    with f2:
        f_inicio_sintomas = st.date_input("🤒 Inicio de síntomas IAAS", value=None, format="DD/MM/YYYY")
        f_deteccion = st.date_input("🔍 Detección de la IAAS", value=None, format="DD/MM/YYYY")
    with f3:
        f_resolucion = st.date_input("✅ Resolución de la IAAS", value=None, format="DD/MM/YYYY")
        f_egreso_hosp = st.date_input("🚪 Egreso Hospitalario", value=None, format="DD/MM/YYYY")

    # --- INFORMACIÓN DE EGRESO ---
    motivo_egreso = None
    if f_egreso_hosp:
        st.subheader("3. Información de Egreso")
        motivo_egreso = st.selectbox("Motivo de egreso", ["Perdida de vigencia", "Mejoria", "Alta voluntaria", "Referencia a otro hospital", "Defunción", "Abandono no autorizado"], index=None, placeholder="Seleccione...")

        if motivo_egreso == "Defunción":
            st.warning("⚠️ Registro de Defunción")
            c_def1, c_def2 = st.columns(2)
            f_defuncion = c_def1.date_input("Fecha de defunción", format="DD/MM/YYYY")
            folio_def = c_def1.text_input("Folio de certificado de defunción", key="Folio_Def", on_change=to_upper, args=["Folio_Def"])
            causa_muerte = c_def2.radio("Causa de muerte", ["Por IAAS", "Con IAAS", "Por otra causa"])

  # --- BOTÓN ATRÁS ---
    with col_atras:
        if st.button("⬅️ Atrás"):
            st.session_state.datos_completos["Hosp"] = {
                "Tipo_Ingreso": tipo_ingreso, "Tipo_Servicio": tipo_servicio,
                "Cama": st.session_state.Cama, "Diagnostico_Ingreso": st.session_state.Diag_Ingreso,
                "Servicio_IAAS": servicio_iaas
            }
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx > 0:
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()

    # --- BOTÓN GUARDAR ---
    with col_guardar:
        if st.button("💾 Guardar registro y continuar"):
            if not tipo_ingreso or not tipo_servicio:
                st.error("Por favor, completa los campos obligatorios.")
            else:
                st.session_state.datos_completos["Hosp"] = {
                    "Tipo_Ingreso": tipo_ingreso, "Tipo_Servicio": tipo_servicio,
                    "Cama": st.session_state.Cama, "Diagnostico_Ingreso": st.session_state.Diag_Ingreso,
                    "Servicio_IAAS": servicio_iaas
                }
                idx = ORDEN.index(st.session_state.pagina_actual)
                if idx < len(ORDEN) - 1:
                    st.session_state.pagina_actual = ORDEN[idx + 1]
                    st.rerun()

if __name__ == "__main__":
    render()
