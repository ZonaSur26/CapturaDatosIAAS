import streamlit as st
import sys
from datetime import date
from config import ORDEN

# Función para forzar mayúsculas en tiempo real
def to_upper(key):
    st.session_state[key] = str(st.session_state[key]).upper()

def render():
    st.title("Datos de Hospitalización y Egreso")

    # --- RECUPERACIÓN DE DATOS GUARDADOS ---
    g = st.session_state.datos_completos.get("Hosp", {})

    # --- 1. INFORMACIÓN DE INGRESO ---
    st.subheader("1. Información de Ingreso")
    c1, c2 = st.columns(2)
    with c1:
        tipo_ingreso = st.selectbox("Tipo de ingreso", ["Primera vez", "Reingreso"], index=["Primera vez", "Reingreso"].index(g["Tipo_Ingreso"]) if g.get("Tipo_Ingreso") in ["Primera vez", "Reingreso"] else None, placeholder="Seleccione...")
        tipo_servicio = st.selectbox("Tipo de servicio", ["Hospitalización", "Ambulatorio"], index=["Hospitalización", "Ambulatorio"].index(g["Tipo_Servicio"]) if g.get("Tipo_Servicio") in ["Hospitalización", "Ambulatorio"] else None, placeholder="Seleccione...")
        cama = st.text_input("Nº de Cama", key="Cama", value=g.get("Cama", ""), on_change=to_upper, args=["Cama"])
    
    with c2:
        diagnostico_ingreso = st.text_area("Diagnóstico principal de ingreso", key="Diag_Ingreso", value=g.get("Diagnostico_Ingreso", ""), on_change=to_upper, args=["Diag_Ingreso"])
        
        servicios_iaas = sorted(["ADMINISTRACIÓN DE QUIMIOTERAPIA AMBULATORIA", "AISLADOS", "ANESTESIOLOGÍA", "CARDIOLOGÍA", "CIRUGÍA GENERAL", "CLÍNICA DE HERIDAS Y ESTOMAS", "CONSULTA EXTERNA", "CUNERO", "DERMATOLOGÍA", "DIÁLISIS", "ENDOCRINOLOGÍA", "ENDOSCOPIA", "ESTOMATOLOGÍA", "GASTROENTEROLOGÍA", "GENÉTICA", "GERIATRÍA", "GINECOLOGÍA", "HEMATOLOGÍA", "HEMODIÁLISIS", "INFECTOLOGIA", "INHALOTERAPIA ADULTOS", "INMUNOLOGÍA", "MEDICINA INTERNA", "NEFROLOGÍA", "NEONATOLOGÍA", "NEUMOLOGÍA", "NEUROCIRUGÍA", "NEUROLOGÍA", "OBSTETRICIA", "OFTALMOLOGÍA", "ONCOLOGÍA", "ORTOPEDIA", "OTORRINOLARINGOLOGÍA", "PEDIATRÍA", "PSIQUIATRÍA", "REHABILITACIÓN", "REUMATOLOGÍA", "TERAPIA INTENSIVA ADULTO", "URGENCIAS", "UROLOGÍA"])
        servicio_iaas = st.selectbox("Servicio donde adquirió la IAAS", servicios_iaas, index=servicios_iaas.index(g["Servicio_IAAS"]) if g.get("Servicio_IAAS") in servicios_iaas else None, placeholder="Seleccione...")

    # --- 2. CRONOLOGÍA DE FECHAS ---
    st.subheader("2. Cronología de Fechas")
    f1, f2, f3 = st.columns(3)
    with f1:
        f_ingreso_hosp = st.date_input("🏥 Ingreso Hospitalario", value=g.get("F_Ingreso_Hosp", None), format="DD/MM/YYYY")
        f_ingreso_serv = st.date_input("🩺 Ingreso al servicio (IAAS)", value=g.get("F_Ingreso_Serv", None), format="DD/MM/YYYY")
    with f2:
        f_inicio_sintomas = st.date_input("🤒 Inicio de síntomas IAAS", value=g.get("F_Inicio_Sint", None), format="DD/MM/YYYY")
        f_deteccion = st.date_input("🔍 Detección de la IAAS", value=g.get("F_Deteccion", None), format="DD/MM/YYYY")
    with f3:
        f_resolucion = st.date_input("✅ Resolución de la IAAS", value=g.get("F_Resolucion", None), format="DD/MM/YYYY")
        f_egreso_hosp = st.date_input("🚪 Egreso Hospitalario", value=g.get("F_Egreso_Hosp", None), format="DD/MM/YYYY")

    # --- 3. INFORMACIÓN DE EGRESO ---
    motivo_egreso = None
    if f_egreso_hosp:
        st.subheader("3. Información de Egreso")
        motivos = ["Perdida de vigencia", "Mejoria", "Alta voluntaria", "Referencia a otro hospital", "Defunción", "Abandono no autorizado"]
        motivo_egreso = st.selectbox("Motivo de egreso", motivos, index=motivos.index(g["Motivo_Egreso"]) if g.get("Motivo_Egreso") in motivos else None, placeholder="Seleccione...")

        if motivo_egreso == "Defunción":
            st.warning("⚠️ Registro de Defunción")
            c_def1, c_def2 = st.columns(2)
            f_defuncion = c_def1.date_input("Fecha de defunción", value=g.get("F_Defuncion", None), format="DD/MM/YYYY")
            folio_def = c_def1.text_input("Folio de certificado de defunción", key="Folio_Def", value=g.get("Folio_Def", ""), on_change=to_upper, args=["Folio_Def"])
            causa_muerte = c_def2.radio("Causa de muerte", ["Por IAAS", "Con IAAS", "Por otra causa"], index=["Por IAAS", "Con IAAS", "Por otra causa"].index(g["Causa_Muerte"]) if g.get("Causa_Muerte") in ["Por IAAS", "Con IAAS", "Por otra causa"] else None)

    # --- NAVEGACIÓN Y GUARDADO ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])
    
    with col_atras:
        if st.button("⬅️ Atrás"):
            st.session_state.datos_completos["Hosp"] = {
                "Tipo_Ingreso": tipo_ingreso, "Tipo_Servicio": tipo_servicio,
                "Cama": st.session_state.Cama, "Diagnostico_Ingreso": st.session_state.Diag_Ingreso,
                "Servicio_IAAS": servicio_iaas, "F_Ingreso_Hosp": f_ingreso_hosp, 
                "F_Ingreso_Serv": f_ingreso_serv, "F_Inicio_Sint": f_inicio_sintomas,
                "F_Deteccion": f_deteccion, "F_Resolucion": f_resolucion, 
                "F_Egreso_Hosp": f_egreso_hosp, "Motivo_Egreso": motivo_egreso
            }
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx > 0:
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()

    with col_guardar:
        if st.button("💾 Guardar registro y continuar"):
            if not all([tipo_ingreso, tipo_servicio]):
                st.error("Por favor, completa los campos obligatorios.")
            else:
                st.session_state.datos_completos["Hosp"] = {
                    "Tipo_Ingreso": tipo_ingreso, "Tipo_Servicio": tipo_servicio,
                    "Cama": st.session_state.Cama, "Diagnostico_Ingreso": st.session_state.Diag_Ingreso,
                    "Servicio_IAAS": servicio_iaas, "F_Ingreso_Hosp": f_ingreso_hosp,
                    "F_Ingreso_Serv": f_ingreso_serv, "F_Inicio_Sint": f_inicio_sintomas,
                    "F_Deteccion": f_deteccion, "F_Resolucion": f_resolucion, 
                    "F_Egreso_Hosp": f_egreso_hosp, "Motivo_Egreso": motivo_egreso
                }
                idx = ORDEN.index(st.session_state.pagina_actual)
                if idx < len(ORDEN) - 1:
                    st.session_state.pagina_actual = ORDEN[idx + 1]
                    st.rerun()

if __name__ == "__main__":
    render()
