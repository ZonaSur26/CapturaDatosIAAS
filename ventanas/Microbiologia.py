import streamlit as st

def render():
    st.title("Diagnóstico Microbiológico")

    # --- 1. HEMOCULTIVOS (Condicional) ---
    st.markdown("*Hemocultivos solo para ITS*")
    hemocultivo_its = st.radio("¿Se tomaron hemocultivos para ITS?", ["No", "Sí"], index=None, horizontal=True)
    if hemocultivo_its == "Sí":
        s_periferica = st.checkbox("SANGRE PERIFÉRICA")
        s_cateter = st.checkbox("SANGRE POR CATETÉR CENTRAL")
        p_cateter = st.checkbox("PUNTA DE CATETÉR CENTRAL")

    # --- 2. PREGUNTA GENERAL ---
    se_tomo_muestra = st.radio("¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", ["No", "Sí"], index=None, horizontal=True)

    if se_tomo_muestra == "Sí" or hemocultivo_its == "Sí":
        # --- A. DATOS GENERALES DE LA MUESTRA ---
        c1, c2 = st.columns(2)
        with c1:
            fecha_toma = st.date_input("FECHA DE TOMA")
            lab_opciones = ["De la unidad", "InDRE", "LESP", "LAVE", "PRIVADO/SUBROGADO", "OTRO"]
            laboratorio = st.selectbox("LABORATORIO", lab_opciones, index=None)
            if laboratorio == "OTRO":
                otro_lab = st.text_input("Especifique otro laboratorio:")
        with c2:
            fecha_resultado = st.date_input("FECHA DE RESULTADO")
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
            tipo_muestra = st.selectbox("TIPO DE MUESTRA", muestras_opciones, index=None)
            if tipo_muestra == "Otro":
                otra_muestra = st.text_input("Especifique otro tipo de muestra:")

        # --- B. SUSCEPTIBILIDAD ---
        st.subheader("Susceptibilidad Antimicrobiana")
        realizo_susceptibilidad = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD ANTIMICROBIANA?", ["No", "Sí"], index=None, horizontal=True)
        
        if realizo_susceptibilidad == "Sí":
            st.selectbox("TÉCNICA PARA SUSCEPTIBILIDAD", ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"], index=None)
            st.markdown("*Leyenda: S=Susceptible, I=Intermedio, R=Resistente, ND=No determinada. *CMI= Concentración mínima inhibitoria")
            
            antibioticos = ["AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", "AZTREONAM",
                            "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA",
                            "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANE-TAZOBACTAM",
                            "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", "DAPTOMICINA",
                            "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA",
                            "IMIPENEM", "ITRACONAZOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "MICAFUNGINA",
                            "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM",
                            "POSACONAZOL", "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA",
                            "TRIMETOPRIM-SULFAMETOXAZOL", "VANCOMICINA", "VORICONAZOL"]
            
            h1, h2, h3 = st.columns([3, 4, 2])
            h1.write("**ANTIMICROBIANO**"); h2.write("**S / I / R / ND**"); h3.write("**CMI**")
            
            for ab in antibioticos:
                c1, c2, c3 = st.columns([3, 4, 2])
                c1.write(ab)
                c2.radio(f"Resistencia {ab}", ["S", "I", "R", "ND"], key=f"res_{ab}", horizontal=True, label_visibility="collapsed")
                c3.text_input(f"CMI {ab}", key=f"cmi_{ab}", label_visibility="collapsed")

        # --- C. TÉCNICA GENERAL Y RESULTADO ---
        st.subheader("Resultado Final")
        tecnicas = ["Bioquímicas manuales", "Inmunocromatografía", "Manuales API", "Semi-automatizados (AutoScan)", 
                    "VITEK (automatizada)", "MicroScan (automatizada)", "Aries Sensititre (automatizada)", 
                    "Phoenix (automatizada)", "Espectrometría de masas. MALDI-TOF", "PCR (moleculares)", 
                    "Sondas de hibridación (moleculares)"]
        st.selectbox("TÉCNICA PARA DIAGNÓSTICO MICROBIOLÓGICO", tecnicas, index=None)
        resultado = st.radio("RESULTADO", ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"], index=None)

        if resultado == "CON DESARROLLO/ POSITIVO":
            # (Aquí puedes incluir tu lista completa de microorganismos)
            micro = st.selectbox("MICROORGANISMO AISLADO", ["Acinetobacter baumannii", "Escherichia coli", "Otros"], index=None)
            if micro == "Otros": st.text_input("Especifique microorganismo:")

        if st.button("Guardar Microbiología"):
            st.success("Datos guardados.")
