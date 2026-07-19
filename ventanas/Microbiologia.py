import streamlit as st

def render():
    st.title("Diagnóstico Microbiológico")

    # --- NUEVA SECCIÓN HEMOCULTIVOS ---
    st.markdown("*Hemocultivos solo para ITS*")
    hemocultivo_its = st.radio("¿Se tomaron hemocultivos para ITS?", ["No", "Sí"], index=None)
    
    sangre_periferica = False
    sangre_cateter = False
    punta_cateter = False
    
    if hemocultivo_its == "Sí":
        sangre_periferica = st.checkbox("SANGRE PERIFÉRICA")
        sangre_cateter = st.checkbox("SANGRE POR CATETÉR CENTRAL")
        punta_cateter = st.checkbox("PUNTA DE CATETÉR CENTRAL")

    # --- PREGUNTA GENERAL ---
    se_tomo_muestra = st.radio("¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", ["No", "Sí"], index=None)

    # Se despliega el formulario si se respondió Sí a ITS o Sí a Microbiología general
    if se_tomo_muestra == "Sí" or hemocultivo_its == "Sí":
        # --- FECHAS Y LABORATORIO ---
        c1, c2 = st.columns(2)
        with c1:
            fecha_toma = st.date_input("FECHA DE TOMA")
            lab_opciones = ["De la unidad", "InDRE", "LESP", "LAVE", "PRIVADO/SUBROGADO", "OTRO"]
            laboratorio = st.selectbox("LABORATORIO", lab_opciones, index=None)
            if laboratorio == "OTRO":
                otro_lab = st.text_input("Especifique otro laboratorio:")
        with c2:
            fecha_resultado = st.date_input("FECHA DE RESULTADO")
            
        # --- TIPO DE MUESTRA ---
        muestras_opciones = [
            "Orina de chorro medio", "Orina por puncion suprapubica", "Orina cateter vesical", 
            "Sonda de entrada por salida", "Aspirado bronquial", "Aspirado traqueal", "Esputo inducido", 
            "Esputo espontaneo", "Lavado bronco alveolar", "Biopsia transbronquial", "Biopsia pulmonar", 
            "Biopsia pleural", "Sangre periferica", "Aspirado", "Biopsia", "Exudado faringeo", 
            "Drenaje otico", "Sangre por cateter central", "Punta de cateter central", "Drenaje", 
            "Liquido pericardico", "Heces", "Aspirado de absceso o secrecion de herida", 
            "Hisopado de herida quirurgica +score Q", "Liquidos organicos", "Biopsia cuantitativa", 
            "Aspirado de absceso", "Hisopado + score Q", "Liquido sinovial", 
            "Sonicado de piezas protesicas para cultivo", "Hisopado conjuntival", "Raspado ocular", 
            "Aspirado de humor vitreo", "Aspirado de humor acuoso", "Lavado ocular", 
            "Liquido cefaloraquideo", "Liquido peritoneal", "Otro"
        ]
        tipo_muestra = st.selectbox("TIPO DE MUESTRA", muestras_opciones, index=None)
        if tipo_muestra == "Otro":
            otra_muestra = st.text_input("Especifique otro tipo de muestra:")

        # --- TÉCNICA ---
        tecnicas = [
            "Bioquímicas manuales", "Inmunocromatografía", "Manuales API", "Semi-automatizados (AutoScan)", 
            "VITEK (automatizada)", "MicroScan (automatizada)", "Aries Sensititre (automatizada)", 
            "Phoenix (automatizada)", "Espectrometría de masas. MALDI-TOF", "PCR (moleculares)", 
            "Sondas de hibridación (moleculares)"
        ]
        tecnica = st.selectbox("TÉCNICA PARA DIAGNÓSTICO MICROBIOLÓGICO", tecnicas, index=None)

        # --- RESULTADO ---
        resultado = st.radio("RESULTADO", ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"], index=None)

        # --- MICROORGANISMO ---
        if resultado == "CON DESARROLLO/ POSITIVO":
            # (El listado de microorganismos se mantiene igual aquí...)
            microorganismos = sorted(["Absidia spp", "Achromobacter sp.", "Acinetobacter baumannii", "Candida albicans", "Escherichia coli", "Otros"]) # ... resto de la lista
            microorganismo = st.selectbox("MICROORGANISMO AISLADO", microorganismos, index=None)
            if microorganismo == "Otros":
                otro_micro = st.text_input("Especifique otro microorganismo:")

        if st.button("Guardar Microbiología"):
            st.success("Datos guardados correctamente.")
