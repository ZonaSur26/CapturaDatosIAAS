import streamlit as st
import sys

def render():
    st.title("IAAS y Factores de Riesgo")

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
        tipo_iaas = st.selectbox("Tipo de IAAS", lista_iaas, index=None, placeholder="Seleccione...")
        otro_iaas = st.text_input("Especifique la IAAS:") if tipo_iaas == "OTRO" else ""
            
        tipo_deteccion = st.selectbox("Tipo de detección", ["Definida clinicamente", "Confirmada por laboratorio"], index=None, placeholder="Seleccione...")
    
    brote = st.radio("¿El caso forma parte de un brote?", ["No", "Sí"], index=None, horizontal=True)
    folio_brote = st.text_input("Folio NOTINMED") if brote == "Sí" else ""

    # --- CIRUGÍAS ---
    st.subheader("Cirugías relacionadas con la IAAS")
    cirugias_data = []
    for i in range(1, 5):
        with st.expander(f"Captura de Cirugía {i}"):
            cols = st.columns(3)
            f_cir = cols[0].date_input(f"Fecha de cirugía {i}", key=f"f_cir_{i}", value=None, format="DD/MM/YYYY")
            t_cir = cols[0].selectbox(f"Tipo {i}", ["Electiva", "Urgencia"], key=f"tipo_cir_{i}", index=None)
            grado = cols[1].selectbox(f"Grado {i}", ["Limpia", "Limpia con implante", "Limpia contaminada", "Contaminada", "Sucia"], key=f"grado_{i}", index=None)
            prot = cols[1].radio(f"Prótesis {i}", ["No", "Sí"], horizontal=True, key=f"protesis_{i}", index=None)
            proc = cols[2].text_input(f"Procedimiento {i}", key=f"proc_{i}")
            
            if f_cir:
                cirugias_data.append({"Fecha": f_cir.strftime("%d/%m/%Y"), "Tipo": t_cir, "Grado": grado, "Protesis": prot, "Procedimiento": proc})

    # --- FACTORES (Resumen para guardado) ---
    st.subheader("Factores de riesgo")
    # Nota: Los campos de factores (i=1..5) se acceden vía st.session_state[f"c_{i}"] en el guardado

    # --- ACCIÓN ---
    if st.button("Guardar registro y continuar"):
        if not tipo_iaas or not tipo_deteccion:
            st.error("Por favor, completa el tipo de IAAS y el tipo de detección.")
        else:
            st.session_state.datos_completos["IAAS"] = {
                "Tipo": tipo_iaas,
                "Otro": otro_iaas,
                "Deteccion": tipo_deteccion,
                "Brote": brote,
                "Folio": folio_brote,
                "Cirugias": cirugias_data
            }
            
            # Navegación automática segura
            main_module = sys.modules['main']
            ORDEN = main_module.ORDEN
            indice = ORDEN.index(st.session_state.pagina_actual)
            
            if indice < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[indice + 1]
                st.success("Guardado. Redirigiendo...")
                st.rerun()

if __name__ == "__main__":
    render()
