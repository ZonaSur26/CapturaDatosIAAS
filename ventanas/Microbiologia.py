import streamlit as st
import sys

def render():
    st.set_page_config(layout="wide")
    st.title("Diagnóstico Microbiológico")

    # --- 0. RECUPERACIÓN DE ESTADOS (DE IAAS.PY) ---
    hab_micro = st.session_state.get("habilitar_microbiologia", False)
    hab_hemo = st.session_state.get("habilitar_hemocultivos", False)

    if not hab_micro:
        st.warning("⚠️ Los campos de microbiología están inhabilitados porque la detección fue 'Definida clínicamente'.")

    # --- CSS PARA EL SOMBREADO ---
    st.markdown("""
        <style>
        .highlight-row {
            background-color: #e6f3ff;
            padding: 5px 10px;
            border-radius: 8px;
            margin-bottom: 2px;
            border: 1px solid #d1e7fd;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. HEMOCULTIVOS (ITS) ---
    st.markdown("### Hemocultivos")
    hemocultivo_its = st.radio(
        "¿Se tomaron hemocultivos para ITS?", 
        ["No", "Sí"], 
        index=None, 
        horizontal=True,
        disabled=not (hab_micro and hab_hemo)
    )
    
    if hemocultivo_its == "Sí":
        c_hem1, c_hem2, c_hem3 = st.columns(3)
        se_periferica = c_hem1.radio("SANGRE PERIFÉRICA", ["No", "Sí"], index=None, horizontal=True)
        se_cateter = c_hem2.radio("SANGRE POR CATETÉR CENTRAL", ["No", "Sí"], index=None, horizontal=True)
        se_punta = c_hem3.radio("PUNTA DE CATETÉR CENTRAL", ["No", "Sí"], index=None, horizontal=True)

    # --- 2. PREGUNTA GENERAL ---
    se_tomo_muestra = st.radio(
        "¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", 
        ["No", "Sí"], 
        index=None, 
        horizontal=True,
        disabled=not hab_micro
    )

    if (se_tomo_muestra == "Sí" or hemocultivo_its == "Sí") and hab_micro:
        
        # --- A. DATOS DE LA MUESTRA ---
        c1, c2 = st.columns(2)
        with c1:
            fecha_toma = st.date_input("FECHA DE TOMA", value=None, format="DD/MM/YYYY")
            lab_opciones = ["De la unidad", "InDRE", "LESP", "LAVE", "PRIVADO/SUBROGADO", "OTRO"]
            laboratorio = st.selectbox("LABORATORIO", lab_opciones, index=None, placeholder="Seleccione...")
            if laboratorio == "OTRO":
                otro_lab = st.text_input("Especifique otro laboratorio:")
        with c2:
            fecha_resultado = st.date_input("FECHA DE RESULTADO", value=None, format="DD/MM/YYYY")
            muestras_opciones = ["Orina de chorro medio", "Orina por puncion suprapubica", "Orina cateter vesical", 
                                 "Sonda de entrada por salida", "Aspirado bronquial", "Aspirado traqueal", 
                                 "Esputo inducido", "Esputo espontaneo", "Lavado bronco alveolar", "Biopsia transbronquial", 
                                 "Biopsia pulmonar", "Biopsia pleural", "Sangre periferica", "Aspirado", "Biopsia", 
                                 "Exudado faringeo", "Drenaje otico", "Sangre por cateter central", "Punta de cateter central", 
                                 "Drenaje", "Liquido pericardico", "Heces", "Aspirado de absceso o secrecion de herida", 
                                 "Hisopado de herida quirurgica +score Q", "Liquidos organicos", "Biopsia cuantitativa", 
                                 "Aspirado de absceso", "Hisopado + score Q", "Liquido sinovial", 
                                 "Sonicado de piezas protesicas para cultivo", "Hisopado conjuntival", "Raspado ocular", 
                                 "Aspirado de humor vitreo", "Aspirado de humor acuoso", "Lavado ocular", 
                                 "Liquido cefaloraquideo", "Liquido peritoneal", "Otro"]
            tipo_muestra = st.selectbox("TIPO DE MUESTRA", muestras_opciones, index=None, placeholder="Seleccione...")
            if tipo_muestra == "Otro":
                otra_muestra = st.text_input("Especifique otro tipo de muestra:")

        # --- B. TÉCNICA Y RESULTADO ---
        tecnicas = ["Bioquímicas manuales", "Inmunocromatografía", "Manuales API", "Semi-automatizados (AutoScan)", 
                    "VITEK (automatizada)", "MicroScan (automatizada)", "Aries Sensititre (automatizada)", 
                    "Phoenix (automatizada)", "Espectrometría de masas. MALDI-TOF", "PCR (moleculares)", 
                    "Sondas de hibridación (moleculares)"]
        st.selectbox("TÉCNICA PARA DIAGNÓSTICO MICROBIOLÓGICO", tecnicas, index=None, placeholder="Seleccione...")
        
        resultado = st.radio("RESULTADO", ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"], index=None)

        if resultado == "CON DESARROLLO/ POSITIVO":
            # (Tu lista original de microorganismos aquí...)
            micro = st.selectbox("MICROORGANISMO AISLADO", ["Staphylococcus aureus", "Otros"], index=None, placeholder="Seleccione...")
            if micro == "Otros": 
                st.text_input("Especifique otro microorganismo:")

        # --- C. SUSCEPTIBILIDAD ---
        st.subheader("Prueba de Susceptibilidad")
        realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD ANTIMICROBIANA?", ["No", "Sí"], index=None, horizontal=True)
        
        if realizo_susp == "Sí":
            st.selectbox("TÉCNICA PARA SUSCEPTIBILIDAD", ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"], index=None, placeholder="Seleccione...")
            
            antibioticos = ["AMPICILINA", "VANCOMICINA", "MEROPENEM"] # (Usa tu lista completa aquí)
            for ab in antibioticos:
                key_check = f"check_{ab}"
                row_style = "highlight-row" if st.session_state.get(key_check, False) else ""
                with st.container():
                    st.markdown(f'<div class="{row_style}">', unsafe_allow_html=True)
                    col1, col2, col3, col4 = st.columns([0.5, 2, 2, 1])
                    is_selected = col1.checkbox("", key=key_check)
                    col2.markdown(f"**{ab}**")
                    if is_selected:
                        res = col3.radio(f"Res_{ab}", ["S", "I", "R", "ND"], key=f"res_{ab}", index=None, horizontal=True, label_visibility="collapsed")
                        if res and res != "ND":
                            col4.text_input(f"CMI_{ab}", key=f"cmi_{ab}", label_visibility="collapsed")
                    st.markdown('</div>', unsafe_allow_html=True)

        st.write("---")
        st.radio("¿SE REALIZÓ PRUEBA COMPLEMENTARIA PARA LA IDENTIFICACIÓN DE RESISTENCIA ANTIMICROBIANA?", ["No", "Sí"], index=None, horizontal=True)

    # --- ACCIÓN ---
    if st.button("Guardar registro y continuar"):
        st.session_state.datos_completos["Micro"] = {"Tomada": se_tomo_muestra}
        
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
