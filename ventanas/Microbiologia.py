import streamlit as st
import sys

def render():
    st.set_page_config(layout="wide")
    st.title("Diagnóstico Microbiológico")

    # --- 1. RECUPERACIÓN DE CONDICIONES (DE IAAS.PY) ---
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
            otro_lab = st.text_input("Especifique otro laboratorio:") if laboratorio == "OTRO" else ""
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
            otra_muestra = st.text_input("Especifique otro tipo de muestra:") if tipo_muestra == "Otro" else ""

        # --- B. TÉCNICA Y RESULTADO ---
        tecnicas = ["Bioquímicas manuales", "Inmunocromatografía", "Manuales API", "Semi-automatizados (AutoScan)", 
                    "VITEK (automatizada)", "MicroScan (automatizada)", "Aries Sensititre (automatizada)", 
                    "Phoenix (automatizada)", "Espectrometría de masas. MALDI-TOF", "PCR (moleculares)", 
                    "Sondas de hibridación (moleculares)"]
        tecnica_diag = st.selectbox("TÉCNICA PARA DIAGNÓSTICO MICROBIOLÓGICO", tecnicas, index=None, placeholder="Seleccione...")
        
        resultado = st.radio("RESULTADO", ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"], index=None)

        if resultado == "CON DESARROLLO/ POSITIVO":
            microorganismos = ["Staphylococcus aureus", "Escherichia coli", "Pseudomonas aeruginosa", "Candida albicans", "Otros"] # (Reducido por brevedad aquí, usa tu lista original)
            micro = st.selectbox("MICROORGANISMO AISLADO", microorganismos, index=None, placeholder="Seleccione...")
            otro_micro = st.text_input("Especifique otro microorganismo:") if micro == "Otros" else ""

        # --- C. SUSCEPTIBILIDAD ---
        st.subheader("Prueba de Susceptibilidad")
        realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD ANTIMICROBIANA?", ["No", "Sí"], index=None, horizontal=True)
        
        if realizo_susp == "Sí":
            st.selectbox("TÉCNICA PARA SUSCEPTIBILIDAD", ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"], index=None, placeholder="Seleccione...")
            st.markdown("*Leyenda: S=Susceptible. I= Intermedio. R= Resistente. ND= No determinada.*")
            
            # (Mantén aquí tu lógica de bucle para antibióticos original)

    # --- ACCIÓN DE GUARDADO ---
    if st.button("Guardar registro y continuar"):
        # Guardado en contenedor global
        st.session_state.datos_completos["Micro"] = {
            "Hemocultivo_ITS": hemocultivo_its,
            "Se_tomo_muestra": se_tomo_muestra
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
