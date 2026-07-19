import streamlit as st

def render():
    st.title("Diagnóstico Microbiológico")

    # --- 1. HEMOCULTIVOS (ITS) ---
    st.markdown("*Hemocultivos solo para ITS*")
    # Al no poner index, Streamlit no selecciona nada por defecto
    hemocultivo_its = st.radio("¿Se tomaron hemocultivos para ITS?", ["No", "Sí"], index=None, horizontal=True)
    
    if hemocultivo_its == "Sí":
        s_periferica = st.radio("SANGRE PERIFÉRICA", ["No", "Sí"], index=None, horizontal=True)
        s_cateter = st.radio("SANGRE POR CATETÉR CENTRAL", ["No", "Sí"], index=None, horizontal=True)
        p_cateter = st.radio("PUNTA DE CATETÉR CENTRAL", ["No", "Sí"], index=None, horizontal=True)

    # --- 2. PREGUNTA GENERAL ---
    se_tomo_muestra = st.radio("¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", ["No", "Sí"], index=None, horizontal=True)

    if se_tomo_muestra == "Sí" or hemocultivo_its == "Sí":
        
        # --- A. DATOS DE LA MUESTRA ---
        c1, c2 = st.columns(2)
        with c1:
            fecha_toma = st.date_input("FECHA DE TOMA", value=None)
            lab_opciones = ["De la unidad", "InDRE", "LESP", "LAVE", "PRIVADO/SUBROGADO", "OTRO"]
            laboratorio = st.selectbox("LABORATORIO", lab_opciones, index=None, placeholder="Seleccione...")
            if laboratorio == "OTRO":
                otro_lab = st.text_input("Especifique otro laboratorio:")
        with c2:
            fecha_resultado = st.date_input("FECHA DE RESULTADO", value=None)
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
            microorganismos = sorted(["Acinetobacter baumannii", "Candida auris", "Escherichia coli", "Klebsiella pneumoniae", "Pseudomonas aeruginosa", "Staphylococcus aureus", "Otros"]) 
            micro = st.selectbox("MICROORGANISMO AISLADO", microorganismos, index=None, placeholder="Seleccione...")
            if micro == "Otros": st.text_input("Especifique microorganismo:")

        # --- C. SUSCEPTIBILIDAD ---
        st.subheader("Prueba de Susceptibilidad")
        realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD ANTIMICROBIANA?", ["No", "Sí"], index=None, horizontal=True)
        
        if realizo_susp == "Sí":
            st.selectbox("TÉCNICA PARA SUSCEPTIBILIDAD", ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"], index=None, placeholder="Seleccione...")
            st.markdown("*Leyenda: S=Susceptible. I= Intermedio. R= Resistente. ND= No determinada. *CMI= Concentración mínima inhibitoria")
            
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
                # radio con index=None deja el radio vacio
                c2.radio(f"Res_{ab}", ["S", "I", "R", "ND"], key=f"res_{ab}", index=None, horizontal=True, label_visibility="collapsed")
                c3.text_input(f"CMI_{ab}", key=f"cmi_{ab}", label_visibility="collapsed")

        if st.button("Guardar Microbiología"):
            st.success("Datos guardados.")
