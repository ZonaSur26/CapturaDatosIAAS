import streamlit as st
import sys
from config import ORDEN

def render():
    st.title("IAAS y Factores de Riesgo")

    # --- RECUPERACIÓN DE DATOS (Persistencia) ---
    g = st.session_state.datos_completos.get("IAAS", {})

    # --- CLASIFICACIÓN ---
    st.subheader("Clasificación de la IAAS")
    c1, c2 = st.columns(2)
    with c1:
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
        
        # KEY corregida para coincidir con la lógica
        tipo_iaas = st.selectbox("Tipo de IAAS", lista_iaas, key="tipo_iaas", index=lista_iaas.index(g.get("tipo_iaas")) if g.get("tipo_iaas") in lista_iaas else None, placeholder="Seleccione...")
        
        otro_iaas = st.text_input("Especifique la IAAS:", key="otro_iaas", value=g.get("otro_iaas", "")) if tipo_iaas == "OTRO" else ""
            
        # KEY corregida
        tipo_deteccion = st.selectbox("Tipo de detección", ["Definida clinicamente", "Confirmada por laboratorio"], key="tipo_deteccion", index=["Definida clinicamente", "Confirmada por laboratorio"].index(g.get("tipo_deteccion")) if g.get("tipo_deteccion") in ["Definida clinicamente", "Confirmada por laboratorio"] else None, placeholder="Seleccione...")
    
    # KEY corregida
    brote = st.radio("¿El caso forma parte de un brote?", ["No", "Sí"], key="brote", index=["No", "Sí"].index(g.get("brote")) if g.get("brote") in ["No", "Sí"] else None, horizontal=True)
    folio_brote = st.text_input("Folio NOTINMED", key="folio_brote", value=g.get("folio_brote", "")) if brote == "Sí" else ""

    # --- CIRUGÍAS Y FACTORES ---
    # (Mantén aquí tu código de expanders y loops, asegurando que tengan keys consistentes)

    # --- LÓGICA DE GUARDADO ---
    def guardar():
        st.session_state.datos_completos["IAAS"] = {
            "tipo_iaas": st.session_state.get("tipo_iaas"),
            "tipo_deteccion": st.session_state.get("tipo_deteccion"),
            "brote": st.session_state.get("brote"),
            "otro_iaas": st.session_state.get("otro_iaas", ""),
            "folio_brote": st.session_state.get("folio_brote", "")
        }

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
        if st.button("Guardar registro y continuar"):
            # Validación segura usando .get()
            if not st.session_state.get("tipo_iaas") or not st.session_state.get("tipo_deteccion"):
                st.error("Por favor, selecciona los campos obligatorios.")
            else:
                guardar()
                idx = ORDEN.index(st.session_state.pagina_actual)
                if idx < len(ORDEN) - 1:
                    st.session_state.pagina_actual = ORDEN[idx + 1]
                    st.rerun()

if __name__ == "__main__":
    render()
