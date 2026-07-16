import streamlit as st
from datetime import date

def render():
    st.title("Datos de Hospitalización y Egreso")

    # --- INFORMACIÓN DE INGRESO ---
    st.subheader("1. Información de Ingreso")
    c1, c2 = st.columns(2)
    with c1:
        tipo_ingreso = st.selectbox("Tipo de ingreso", ["Primera vez", "Reingreso"], index=None, placeholder="Seleccione...")
        tipo_servicio = st.selectbox("Tipo de servicio", ["Hospitalización", "Ambulatorio"], index=None, placeholder="Seleccione...")
        cama = st.text_input("Nº de Cama")
    
    with c2:
        diagnostico_ingreso = st.text_area("Diagnóstico principal de ingreso")
        
        # Listado completo de servicios ordenado alfabéticamente
        servicios_iaas = sorted([
            "ADMINISTRACIÓN DE QUIMIOTERAPIA AMBULATORIA", "AISLADOS", "ANESTESIOLOGÍA", "ANESTESIOLOGÍA PEDIÁTRICA", 
            "ANGIOLOGÍA", "ÁREA COVID", "ÁREA COVID HOSPITALIZACIÓN", "ÁREA COVID TERAPIA INTENSIVA", 
            "ÁREA COVID URGENCIAS", "BANCO DE SANGRE", "CARDIOLOGÍA", "CARDIOLOGÍA PEDIÁTRICA", 
            "CIRUGÍA AMBULATORIA", "CIRUGÍA CARDIOVASCULAR", "CIRUGÍA DE TÓRAX", "CIRUGÍA GENERAL", 
            "CIRUGÍA MAXILOFACIAL", "CIRUGÍA OFTÁLMICA", "CIRUGÍA ONCOLÓGICA", "CIRUGÍA ONCOLÓGICA DE CABEZA Y CUELLO", 
            "CIRUGÍA ONCOLÓGICA DE GINECOLOGÍA", "CIRUGÍA ONCOLÓGICA DE NEUMOLOGÍA", 
            "CIRUGÍA ONCOLÓGICA DE PIEL Y PARTES BLANDAS", "CIRUGÍA ONCOLÓGICA DE UROLOGÍA", 
            "CIRUGÍA ONCOLÓGICA GASTROENTEROLOGÍA", "CIRUGÍA ONCOLÓGICA PEDIÁTRICA", 
            "CIRUGÍA ONCOLÓGICA TUMORES DE MAMA", "CIRUGÍA PEDIÁTRICA", "CIRUGÍA PEDIÁTRICA CARDIOVASCULAR", 
            "CIRUGÍA PEDIÁTRICA PLÁSTICA", "CIRUGÍA PEDIÁTRICA TÓRAX Y NEUMOLOGÍA", "CIRUGÍA PLÁSTICA", 
            "CLÍNICA DE ACCESOS VASCULARES CENTRALES", "CLÍNICA DE ENFERMEDADES LISOSOMALES PEDIÁTRICAS", 
            "CLÍNICA DE HERIDAS Y ESTOMAS", "CONSULTA EXTERNA", "CORTA ESTANCIA", "CRECIMIENTO Y DESARROLLO", 
            "CUIDADOS INTENSIVOS NEONATALES EXTERNOS", "CUNERO", "CUNERO PATOLÓGICO", "DERMATOLOGÍA", 
            "DERMATOLOGÍA PEDIÁTRICA", "DIÁLISIS", "ENDOCRINOLOGÍA", "ENDOCRINOLOGÍA PEDIÁTRICA", "ENDOSCOPIA", 
            "ENDOSCOPIA PEDIÁTRICA", "ESTOMATOLOGÍA", "ESTOMATOLOGÍA PEDIÁTRICA", "GASTROCIRUGÍA", 
            "GASTROENTEROLOGÍA", "GASTROENTEROLOGÍA PEDIÁTRICA", "GASTRONUTRICIÓN", "GENÉTICA", 
            "GENÉTICA PEDIÁTRICA", "GERIATRÍA", "GINECOLOGÍA", "GINECOLOGÍA Y OBSTETRICIA", "HABITACIÓN CONJUNTA", 
            "HEMATOLOGÍA", "HEMATOLOGÍA PEDIÁTRICA", "HEMATONCOLÓGICA", "HEMATONCOLÓGICA PEDIÁTRICA", 
            "HEMODIÁLISIS", "HEMODIÁLISIS PEDIÁTRICA", "HEMODINÁMICA", "HEMODINÁMICA PEDIÁTRICA", 
            "INFECTOLOGIA", "INFECTOLOGIA PEDIÁTRICA", "INHALOTERAPIA ADULTOS", "INHALOTERAPIA PEDIÁTRICA", 
            "INMUNOLOGÍA", "INMUNOLOGÍA PEDIÁTRICA", "INMUNOTERAPIA DE CORTA ESTANCIA", 
            "INMUNOTERAPIA DE CORTA ESTANCIA PEDIÁTRICA", "LACTANTES", "MEDICINA INTERNA", "MEDICINA NUCLEAR", 
            "NEFROLOGÍA", "NEFROLOGÍA PEDIÁTRICA", "NEONATOLOGÍA", "NEUMOLOGÍA", "NEUMOLOGÍA PEDIÁTRICA", 
            "NEUROCIRUGÍA", "NEUROCIRUGÍA ONCOLÓGICA", "NEUROCIRUGÍA PEDIÁTRICA", "NEUROLOGÍA", 
            "NEUROLOGÍA PEDIÁTRICA", "OBSTETRICIA", "ODONTOLOGÍA", "OFTALMOLOGÍA", "OFTALMOLOGÍA PEDIÁTRICA", 
            "ONCOLOGÍA", "ONCOLOGÍA MEDICA", "ONCOLOGÍA MÉDICA DE CABEZA Y CUELLO", 
            "ONCOLOGÍA MÉDICA DE GASTROENTEROLOGÍA", "ONCOLOGÍA MÉDICA DE NEUMOLOGÍA", 
            "ONCOLOGÍA MÉDICA DE PIEL Y PARTES BLANDAS", "ONCOLOGÍA MÉDICA DE TUMORES DE MAMA", 
            "ONCOLOGÍA MÉDICA DE UROLOGÍA", "ONCOLOGÍA MÉDICA GINECOLOGÍA", "ONCOLOGÍA PEDIÁTRICA", 
            "ORTOPEDIA", "ORTOPEDIA PEDIÁTRICA", "OTORRINOLARINGOLOGÍA", "OTORRINOLARINGOLOGÍA PEDIÁTRICA", 
            "PARASITOLOGÍA PEDIÁTRICA", "PEDIATRÍA", "PERSONAL DE SALUD", "PSIQUIATRÍA", "RADIOLOGÍA INTERVENCIONISTA", 
            "RADIOTERAPIA", "REHABILITACIÓN", "REUMATOLOGÍA", "SERVICIO DE QUEMADOS", "TERAPIA CENTRAL", 
            "TERAPIA DE CARDIOLOGÍA", "TERAPIA DE GINECOOBSTETRICIA", "TERAPIA DE INFECTOLOGIA", 
            "TERAPIA DE NEUMOLOGÍA", "TERAPIA DE NEUROLOGÍA", "TERAPIA DE ONCOLOGÍA", "TERAPIA INTENSIVA ADULTO", 
            "TERAPIA INTENSIVA NEONATAL", "TERAPIA INTENSIVA PEDIÁTRICA", "TERAPIA INTERMEDIA ADULTO", 
            "TERAPIA INTERMEDIA NEONATAL", "TERAPIA INTERMEDIA PEDIÁTRICA", "TRASPLANTES", "TRAUMATOLOGÍA", 
            "UNIDAD DE CUIDADOS CORONARIOS", "UNIDAD DE CUIDADOS INTENSIVOS CARDIOVASCULARES", 
            "UNIDAD DE CUIDADOS INTENSIVOS CARDIOVASCULARES PEDIÁTRICA", "UNIDAD DE CUIDADOS INTENSIVOS PEDIÁTRICOS", 
            "UNIDAD DE TRASPLANTES DE CÉLULAS HEMATOPOYÉTICAS", "UNIDAD METABÓLICA", "URGENCIAS", 
            "URGENCIAS PEDIÁTRICAS", "UROLOGÍA", "UROLOGÍA PEDIÁTRICA"
        ])
        
        servicio_iaas = st.selectbox("Servicio donde adquirió la IAAS", servicios_iaas, index=None, placeholder="Seleccione...")

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
        ], index=None, placeholder="Seleccione...")

        if motivo_egreso == "Defunción":
            st.warning("⚠️ Registro de Defunción")
            c_def1, c_def2 = st.columns(2)
            with c_def1:
                f_defuncion = st.date_input("Fecha de defunción")
                folio_def = st.text_input("Folio de certificado de defunción")
            with c_def2:
                causa_muerte = st.radio("Causa de muerte", ["Por IAAS", "Con IAAS", "Por otra causa"])

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
