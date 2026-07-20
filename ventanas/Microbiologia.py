import streamlit as st

def render():
    st.title("Diagnóstico Microbiológico")

    # --- 1. HEMOCULTIVOS (ITS) ---
    st.markdown("*Hemocultivos solo para ITS*")
    hemocultivo_its = st.radio("¿Se tomaron hemocultivos para ITS?", ["No", "Sí"], index=None, horizontal=True)
    
    if hemocultivo_its == "Sí":
        se_periferica = st.radio("SANGRE PERIFÉRICA", ["No", "Sí"], index=None, horizontal=True)
        se_cateter = st.radio("SANGRE POR CATETÉR CENTRAL", ["No", "Sí"], index=None, horizontal=True)
        se_punta = st.radio("PUNTA DE CATETÉR CENTRAL", ["No", "Sí"], index=None, horizontal=True)

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
            microorganismos = sorted([
                "Absidia spp", "Achromobacter denitrificans", "Achromobacter sp.", "Achromobacter xylosoxidans", 
                "Acinetobacter baumannii", "Acinetobacter baumanni complex", "Acinetobacter calcoaceticus", 
                "Acinetobacter haemolyticus", "Acinetobacter johnsonii", "Acinetobacter junii", "Acinetobacter Iwoffi", 
                "Acinetobacter nosocomialis", "Acinetobacter pittil", "Acinetobacter sp.", "Actinomyces israelii", 
                "Actinomyces meyeri", "Actinomyces naelundii", "Actinomyces odontolyticus", "Actinomyces sp.", 
                "Actinomyces viscosus", "Adenovirus 1", "Aeromonas bestirarum", "Aeromonas caviae", 
                "Aeromonas caviae complex", "Aeromonas hydrophila", "Aeromonas salmonicida", "Aeromonas sp.", 
                "Aeromonas veroni", "Alcaligenes faecalis", "Alcaligenes sp.", "Aspergillus flavus", 
                "Aspergillus fumigatus", "Aspergillus spp.", "Bacillus anthracis", "Bacillus cereus", 
                "Bacillus circulans", "Bacillus sp.", "Bacillus sp., no anthracis", "Bacillus sp., no cereus", 
                "Bacillus subtilis", "Bacillus subtilis sp. complex", "Bacteroides bivius [Prevotella bivia]", 
                "Bacteroides caccae", "Bacteroides distasonis", "Bacteroides eggerrthii", "Bacteroides fragilis", 
                "Bacteroides fragilis group", "Bacteroides ovatus", "Bacteroides sp.", "Bacteroides spp.", 
                "Brevundimonas diminuta", "Brevundimonas vesicularis", "Burkholderia cepacia", 
                "Burkholderia cepacia complex", "Burkholderia gladioli", "Burkholderia sp.", "Candida albicans", 
                "Candida auris", "Candida glabrata", "Candida guilliermondii", "Candida krusei", "Candida lusitaniae", 
                "Candida parapsilosis", "Candida spp", "Candida tropicalis", "Cardiobacterium hominis", 
                "Cardiobacterium sp.", "Chromobacterium violaceum", "Chryseobacterium gleum", 
                "Chryseobacterium indologenes", "Chryseobacterium sp.", "Chryseomonas luteola", 
                "Chryseomonas sp.", "Citrobacter amalonaticus", "Citrobacter braakii", "Citrobacter farmeri", 
                "Citrobacter freundii", "Citrobacter koseri", "Citrobacter sedlakii", "Citrobacter sp.", 
                "Citrobacter wekmanii", "Citrobacter youngae", "Clostridioides difficile", "Comamonas terrigena", 
                "Comamonas testosteroni", "Corynebacterium amycolatum", "Corynebacterium jeikeium", 
                "Corynebacterium sp.", "Corynebacterium striatum", "Corynebacterium urealyticum", 
                "Corynebacterium xerosis", "Coxsackie", "Cronobacter sakazakii", "Cronobacter sp.", 
                "Cryptococcus albidus", "Cryptococcus gattii", "Cryptococcus laurentii", "Cryptococcus spp.", 
                "Cryptosporidium spp.", "Cutibacterium acnes", "Cutibacterium avidum", "Cutibacterium granulosum", 
                "Cutibacterium sp.", "Cyclospora cayetanensis", "Delftia acidovorans", "Delftia sp.", 
                "Edwardsiella sp.", "Edwardsiella tarda", "Elizabethkingia meningoseptica", "Elizabethkingia sp.", 
                "Empedobacter brevis", "Enterobacter aerogenes", "Enterobacter amnigenus", "Enterobacter asburiae", 
                "Enterobacter bugandensis", "Enterobacter cancerogenus", "Enterobacter cloacae", 
                "Enterobacter cloacae complex", "Enterobacter gergoviae", "Enterobacter hormaechei", 
                "Enterobacter kobei", "Enterobacter ludwigi", "Enterobacter sp.", "Enterobius vermicularis", 
                "Enterococcus avium", "Enterococcus casseliflavus", "Enterococcus durans", "Enterococcus faecalis", 
                "Enterococcus faecium", "Enterococcus flavescens", "Enterococcus gallinarum", "Enterococcus hirae", 
                "Enterococcus malodoratus", "Enterococcus mundtiii", "Enterococcus raffinosus", 
                "Enterococcus sacharolyticus", "Enterococcus sp.", "Enterovirus", "Erysipelothrix rhusiopathiae", 
                "Erysipelothrix sp.", "Escherichia coli", "Escherichia coli, serogroup 0157", "Fusarium spp.", 
                "Giardia spp.", "Hafnia alvei", "Hafnia sp.", "Hepatitis A", "Hepatitis B", "Hepatitis C", 
                "Influenza A", "Influenza AH1N1", "Influenza AH3N2", "Influenza B", "Influenza virus", 
                "Klebsiella aerogenes", "Klebsiella oxytoca", "Klebsiella ozaenae", "Klebsiella pneumoniae", 
                "Klebsiella sp.", "Klebsiella varicola", "Kluyvera ascorbata", "Kocuria kristinae", 
                "Kocuria rosea", "Kocuria sp.", "Leclercia adecarboxylata", "Lichteimia spp.", "Malassezia spp.", 
                "Moraxella bovis", "Moraxella lacunata", "Moraxella nonliquefaciens", "Moraxella osloensis", 
                "Moraxella sp.", "Morganella morganii", "Morganella sp.", "Mucor spp.", "Mycobacterium abscessus", 
                "Mycobacterium avium-intracellulare", "Mycobacterium chelonae", "Mycobacterium fortuitum", 
                "Mycobacterium mucogenicum", "Norovirus", "Ochrobactrum anthropi", "Otros", "Pantoea agglomerans", 
                "Pantoea sp.", "Pediculus humanus capitis", "Pediculus humanus corporis", 
                "Peptostreptococcus anaerobius", "Peptostreptococcus russellii", "Peptostreptococcus sp.", 
                "Peptostreptococcus stomatis", "Prevotella oralis", "Prevotella bivia", "Prevotella denticola", 
                "Prevotella disiens", "Prevotella intermedia", "Prevotella loescheii", "Prevotella melaninogenica", 
                "Prevotella sp.", "Proteus hauseri", "Proteus mirabilis", "Proteus penneri", "Proteus sp.", 
                "Proteus vulgaris", "Providencia alcalifaciens", "Providencia rettgeri", "Providencia rustigianii", 
                "Providencia sp.", "Providencia stuartii", "Pseudomonas aeruginosa", "Pseudomonas alcaligenes", 
                "Pseudomonas fluorescens", "Pseudomonas luteola", "Pseudomonas mendocina", 
                "Pseudomonas monteilii", "Pseudomonas putida", "Pseudomonas sp.", "Pseudomonas stutzeri", 
                "Ralstonia ornithinolytica", "Ralstonia pickettii", "Ralstonia sp.", "Raoultella ornithinolytica", 
                "Raoultella planticola", "Rhinovirus", "Rhizobium radiobacter", "Rhizopus spp.", 
                "Rhodotorula spp.", "Rotavirus", "Rubeola", "Saccharomyces cerevisiae", "Salmonella arizona", 
                "Salmonella choleraesuis", "Salmonella enteritidis", "Salmonella paratyphi", "Salmonella sp.", 
                "Salmonella typhi", "Sarampion", "Sarcoptes scabiei", "SARS-COV-2", "Serratia fonticola", 
                "Serratia liquefaciens", "Serratia marcescens", "Serratia odorifera", "Serratia plymuthica", 
                "Serratia rubidaea", "Serratia Sp.", "Shewanella prutrefaciens", "Shigella boydii", 
                "Shigella dysenteriae", "Shigella flexneri", "Shigella sonnei", "Shigella sp.", 
                "Sphingomonas paucimobilis", "Staphylococcus aureus", "Staphylococcus auricularis", 
                "Staphylococcus capitis", "Staphylococcus coagulasa negativo", "Staphylococcus cohnii", 
                "Staphylococcus epidermidis", "Staphylococcus haemolyticus", "Staphylococcus hominis", 
                "Staphylococcus hyicus", "Staphylococcus intermedius", "Staphylococcus kloosii", 
                "Staphylococcus lentus", "Staphylococcus lugdunensis", "Staphylococcus pseudointermedius", 
                "Staphylococcus saccharolyticus", "Staphylococcus saprophyticus", "Staphylococcus schleiferi", 
                "Staphylococcus sciuri", "Staphylococcus simulans", "Staphylococcus Sp.", "Staphylococcus warneri", 
                "Staphylococcus xylosus", "Stenotrophomonas maltophilia", "Streptococcus agalactiae", 
                "Streptococcus alactolyticus", "Streptococcus anginosus", "Streptococcus bovis group", 
                "Streptococcus constellatus", "Streptococcus mitis", "Streptococcus spp.", "Streptococcus thoraltensis", 
                "Streptococcus viridans", "Trichosporon asahii", "Varicela Zoster", "Vibrio alginolyticus", 
                "Vibrio cholerae", "Vibrio fluvialis", "Vibrio parahaemolyticus", "Vibrio sp.", "Vibrio vulnificus", 
                "Virus de Inmunodeficiencia Humana", "Virus sincitial respiratorio"
            ])
            micro = st.selectbox("MICROORGANISMO AISLADO", microorganismos, index=None, placeholder="Seleccione...")
            if micro == "Otros": 
                st.text_input("Especifique otro microorganismo:")

        # --- C. SUSCEPTIBILIDAD ---
        st.subheader("Prueba de Susceptibilidad")
        realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD ANTIMICROBIANA?", ["No", "Sí"], index=None, horizontal=True)
        
        if realizo_susp == "Sí":
            st.selectbox("TÉCNICA PARA SUSCEPTIBILIDAD", ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"], index=None, placeholder="Seleccione...")
            st.markdown("*Leyenda: S=Susceptible. I= Intermedio. R= Resistente. ND= No determinada. *CMI= Se refiere a la concentración mínima inhibitoria")
            
            antibioticos = ["AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", "AZTREONAM",
                            "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA",
                            "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANE-TAZOBACTAM",
                            "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", "DAPTOMICINA",
                            "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA",
                            "IMIPENEM", "ITRACONAZOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "MICAFUNGINA",
                            "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM",
                            "POSACONAZOL", "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA",
                            "TRIMETOPRIM-SULFAMETOXAZOL", "VANCOMICINA", "VORICONAZOL"]
            
           # Ajustamos las columnas para que la última sea pequeña y compacta
            h1, h2, h3 = st.columns([2, 2, 0.5]) 
            h1.write("**ANTIMICROBIANO**")
            h2.write("**S / I / R / ND**")
            h3.write("**CMI**")
            
            for ab in antibioticos:
                c1, c23 = st.columns([2, 3]) # Dividimos en dos: Nombre y todo el resto
                c1.markdown(f"**{ab}**")
                
                # Ponemos el radio y el CMI en la misma columna c23 usando un contenedor horizontal
                subc1, subc2 = c23.columns([3, 2]) 
                seleccion = subc1.radio(f"Res_{ab}", ["S", "I", "R", "ND"], key=f"res_{ab}", index=None, horizontal=True, label_visibility="collapsed")
                
                if seleccion is not None and seleccion != "ND":
                    subc2.text_input(f"CMI_{ab}", key=f"cmi_{ab}", label_visibility="collapsed", placeholder="CMI")

        if st.button("Guardar Microbiología"):
            st.success("Datos guardados correctamente.")
