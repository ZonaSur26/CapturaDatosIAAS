import streamlit as st
import sys
from config import ORDEN

def render():
    st.title("IAAS y Factores de Riesgo")
    
    # Recuperación de datos previos
    g = st.session_state.datos_completos.get("IAAS", {})

    # --- CLASIFICACIÓN ---
    st.subheader("Clasificación de la IAAS")
    c1, c2 = st.columns(2)
    
    lista_iaas = [
        "CONJUNTIVITIS", "EMPIEMA SECUNDARIO A PROCEDIMIENTO", "ENDOCARDITIS", "ENDOFTALMITIS", 
        "ENDOMETRITIS", "ENFERMEDAD DE LYME", "ERISIPELA", "ERITEMA INFECCIOSO", 
        "EXANTEMA SECUNDARIA A MONONUCLEOSIS INFECCIOSA", 
        "FASCITIS NECROSANTE, GANGRENA INFECCIOSA, CELULITIS, MIOSITIS Y LINFADENITIS", 
        "FLEBITIS", "GASTROENTERITIS", "INFECCIÓN DE ÓRGANOS Y ESPACIOS", 
        "INFECCIÓN DE VÍAS URINARIAS ASOCIADA A CATÉTER URINARIO IVU-CU", 
        "INFECCIÓN DE VÍAS URINARIAS NO ASOCIADA A CATÉTER URINARIO", 
        "INFECCIÓN EN PIEL Y TEJIDOS BLANDOS", 
        "INFECCIÓN EN PIEL Y TEJIDOS BLANDOS EN PACIENTES CON QUEMADURAS", 
        "INFECCIÓN INCISIONAL PROFUNDA", "INFECCIÓN INCISIONAL SUPERFICIAL", 
        "INFECCIÓN INTRACRANEAL", "INFECCIÓN PERIPROTÉSICA (POSARTROPLASTÍA DE CADERA O RODILLA)", 
        "INFECCIÓN POR CLOSTRIDIODES DIFICILE (ICD)", "INFECCIONES DE LA BURSA O ARTICULARES", 
        "INFECCIONES DEL SITIO DE INSERCIÓN DEL CATÉTER, TÚNEL O PUERTO SUBCUTÁNEO", 
        "INFECCIONES RELACIONADAS A PROCEDIMIENTOS ENDOSCÓPICOS", 
        "INFECCIONES RELACIONADAS A PROCEDIMIENTOS ODONTOLÓGICOS", 
        "ITS RELACIONADA A CATÉTER CENTRAL (ITS - CC)", 
        "ITS RELACIONADA A POSIBLE CONTAMINACIÓN DE SOLUCIONES, INFUSIONES O MEDICAMENTOS", 
        "ITS RELACIONADA A PROCEDIMIENTO (ITS-RP)", 
        "ITS SECUNDARIO A DAÑO DE LA BARRERA MICOSA (ITS - DBM)", "MEDIASTINITIS", 
        "MENINGITIS O VENTRICULITIS SECUNDARIA A UN PROCEDIMIENTO DEL SNC", 
        "MIOCARDITIS", "NAAS NO RELACIONADA A PROCEDIMIENTO (NAAS - NRP)", 
        "NAAS RELACIONADA A PROCEDIMIENTO (NAAS - RP)", "NEUMONÍA ASOCIADA A VENTILADOR (NAV)", 
        "OSTEOMIELITIS", "OTITIS MEDIA AGUDA", "OTRO", "PERICARDITIS", 
        "PERITONITIS ASOCIADA A DIÁLISIS", 
        "PERITONITIS ASOCIADA A LA INSTALACIÓN DE CATÉTER DE DIÁLISIS PERITONEAL", 
        "RINOFARINGITIS Y FARINGOAMIGDALITIS", "RUBÉOLA", "SARAMPIÓN", 
        "SINDROME DE CHOQUE TÓXICO", "SINDROME DE PIEL ESCALDADA", 
        "SINDROME PIE-MANO-BOCA", "SINUSITIS AGUDA", "STAPHYLOCOCCEMIA", "VARICELA"
    ]

    with c1:
        st.selectbox("Tipo de IAAS", lista_iaas, key="k_tipo_iaas", index=lista_iaas.index(g["Tipo_IAAS"]) if g.get("Tipo_IAAS") in lista_iaas else None)
        if st.session_state.k_tipo_iaas == "OTRO":
            st.text_input("Especifique la IAAS:", key="k_otro_iaas", value=g.get("Otro_IAAS", ""))
            
        st.selectbox("Tipo de detección", ["Definida clinicamente", "Confirmada por laboratorio"], key="k_deteccion", index=["Definida clinicamente", "Confirmada por laboratorio"].index(g["Tipo_Deteccion"]) if g.get("Tipo_Deteccion") in ["Definida clinicamente", "Confirmada por laboratorio"] else None)
    
    st.radio("¿El caso forma parte de un brote?", ["No", "Sí"], key="k_brote", index=["No", "Sí"].index(g["Brote"]) if g.get("Brote") in ["No", "Sí"] else None, horizontal=True)

    # --- LÓGICA DE GUARDADO ---
    def guardar():
        st.session_state.datos_completos["IAAS"] = {
            "Tipo_IAAS": st.session_state.k_tipo_iaas,
            "Tipo_Deteccion": st.session_state.k_deteccion,
            "Brote": st.session_state.k_brote,
            "Otro_IAAS": st.session_state.get("k_otro_iaas", "")
        }
        st.session_state.habilitar_microbiologia = (st.session_state.k_deteccion == "Confirmada por laboratorio")

    # --- NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])
    
    with col_atras:
        if st.button("⬅️ Atrás"):
            guardar()
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx > 0:
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()

    with col_guardar:
        if st.button("💾 Guardar registro y continuar"):
            if not st.session_state.k_tipo_iaas or not st.session_state.k_deteccion:
                st.error("Por favor, selecciona los campos obligatorios.")
            else:
                guardar()
                idx = ORDEN.index(st.session_state.pagina_actual)
                if idx < len(ORDEN) - 1:
                    st.session_state.pagina_actual = ORDEN[idx + 1]
                    st.rerun()

if __name__ == "__main__":
    render()
