import streamlit as st
from config import ORDEN

def render():
    st.title("Diagnóstico Microbiológico")

    # --- 0. RECUPERACIÓN DE ESTADOS ---
    if "datos_completos" not in st.session_state:
        st.session_state.datos_completos = {}

    m = st.session_state.datos_completos.get("Micro", {})

    # Búsqueda segura de índices ignorando mayúsculas/minúsculas
    def buscar_idx(lista, val):
        if not val: return None
        lista_m = [str(x).lower() for x in lista]
        v_c = str(val).lower().strip()
        return lista_m.index(v_c) if v_c in lista_m else None

    # Estilos CSS para resaltar filas seleccionadas en la tabla de antibióticos
    st.markdown("""
        <style>
        .highlight-row { 
            background-color: #e6f3ff !important; 
            padding: 8px; 
            border-radius: 6px; 
            margin-bottom: 4px; 
            border: 1px solid #d1e7fd; 
        }
        </style>
    """, unsafe_allow_html=True)

    # Catálogo maestro de 62 antibióticos
    antibioticos_master = [
        "AMIKACINA", "AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA",
        "AZTREONAM", "AZITROMICINA", "CASPOFUNGINA", "CEFAZOLINA", "CEFEDICOL",
        "CEFEPIME", "CEFIXIMA", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA",
        "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANO-TAZOBACTAM", "CEFTRIAXONA",
        "CEFUROXIMA", "CIPROFLOXACINO", "CLARITROMICINA", "CLINDAMICINA", "CLORANFENICOL",
        "COLISTINA", "DALBAVANCINA", "DAPTOMICINA", "DOXICICLINA", "ERITROMICINA",
        "ERTAPENEM", "ISAVUCONAZOL", "FLUCONAZOL", "FLUCITOSINA", "FOSFOMICINA",
        "GENTAMICINA", "IMIPENEM", "IMIPENEM-RELEBACTAM", "ITRACONAZOL", "LEVOFLOXACINO",
        "LINEZOLID", "MEROPENEM", "MEROPENEM-VABORBACTAM", "METRONIDAZOL", "MICAFUNGINA",
        "MINOCICLINA", "MOXIFLOXACINO", "NITROFURANTOINA", "OXACILINA", "PENICILINA",
        "PIPERACILINA-TAZOBACTAM", "POLIMIXINA B", "POSACONAZOL", "RIFAMPICINA", "TEDIZOLID",
        "TETRACICLINA", "TICARCILINA-CLAVULANATO", "TIGECICLINA", "TOBRAMICINA", "TRIMETOPRIM-SULFAMETOXAZOL",
        "VANCOMICINA", "VORICONAZOL"
    ]

    # --- 1. HEMOCULTIVOS ITS (SECCIÓN INDEPENDIENTE) ---
    with st.container(border=True):
        st.subheader("1. Hemocultivos para ITS")
        hemocultivo_its = st.radio(
            "¿Se tomaron hemocultivos para ITS?", 
            ["No", "Sí"], 
            key="k_hemo_its", 
            index=buscar_idx(["No", "Sí"], m.get("Hemo_ITS", "No")), 
            horizontal=True
        )
        
        if hemocultivo_its == "Sí":
            with st.container(border=True):
                st.markdown("**Origen del hemocultivo:**")
                c_hem1, c_hem2, c_hem3 = st.columns(3)
                c_hem1.radio("SANGRE PERIFÉRICA", ["No", "Sí"], key="sp", index=buscar_idx(["No", "Sí"], m.get("sp", "No")), horizontal=True)
                c_hem2.radio("SANGRE POR CATÉTER CENTRAL", ["No", "Sí"], key="scc", index=buscar_idx(["No", "Sí"], m.get("scc", "No")), horizontal=True)
                c_hem3.radio("PUNTA DE CATÉTER CENTRAL", ["No", "Sí"], key="pcc", index=buscar_idx(["No", "Sí"], m.get("pcc", "No")), horizontal=True)

    # --- 2. MUESTRA MICROBIOLÓGICA GENERAL (SECCIÓN INDEPENDIENTE) ---
    with st.container(border=True):
        st.subheader("2. Muestra Microbiológica")
        se_tomo_muestra = st.radio(
            "¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", 
            ["No", "Sí"], 
            key="k_tomo_muestra", 
            index=buscar_idx(["No", "Sí"], m.get("Tomada", "No")), 
            horizontal=True
        )

        # Variables de control
        micro_sel, otro_micro_val, tecnica_susp_sel = "", "", ""

        if se_tomo_muestra == "Sí":
            c1, c2 = st.columns(2)
            with c1:
                st.date_input("FECHA DE TOMA", key="k_f_toma", value=m.get("Fecha_Toma") or None, format="DD/MM/YYYY")
                lab_opciones = ["De la unidad", "InDRE", "LESP", "LAVE", "PRIVADO/SUBROGADO", "OTRO"]
                st.selectbox("LABORATORIO", lab_opciones, key="k_lab", index=buscar_idx(lab_opciones, m.get("Lab")), placeholder="Seleccione...")
            
            with c2:
                st.date_input("FECHA DE RESULTADO", key="k_f_res", value=m.get("Fecha_Res") or None, format="DD/MM/YYYY")
                muestras_opciones = ["Orina de chorro medio", "Orina por puncion suprapubica", "Orina cateter vesical", "Sonda de entrada por salida", "Aspirado bronquial", "Aspirado traqueal", "Esputo inducido", "Esputo espontaneo", "Lavado bronco alveolar", "Biopsia transbronquial", "Biopsia pulmonar", "Biopsia pleural", "Sangre periferica", "Aspirado", "Biopsia", "Exudado faringeo", "Drenaje otico", "Sangre por cateter central", "Punta de cateter central", "Drenaje", "Liquido pericardico", "Heces", "Aspirado de absceso o secrecion de herida", "Hisopado de herida quirurgica +score Q", "Liquidos organicos", "Biopsia cuantitativa", "Aspirado de absceso", "Hisopado + score Q", "Liquido sinovial", "Sonicado de piezas protesicas para cultivo", "Hisopado conjuntival", "Raspado ocular", "Aspirado de humor vitreo", "Aspirado de humor acuoso", "Lavado ocular", "Liquido cefaloraquideo", "Liquido peritoneal", "Otro"]
                st.selectbox("TIPO DE MUESTRA", muestras_opciones, key="k_muestra", index=buscar_idx(muestras_opciones, m.get("Muestra")), placeholder="Seleccione...")

            tecnicas = ["Bioquímicas manuales", "Inmunocromatografía", "Manuales API", "Semi-automatizados (AutoScan)", "VITEK (automatizada)", "MicroScan (automatizada)", "Aries Sensititre (automatizada)", "Phoenix (automatizada)", "Espectrometría de masas. MALDI-TOF", "PCR (moleculares)", "Sondas de hibridación (moleculares)"]
            st.selectbox("TÉCNICA PARA DIAGNÓSTICO MICROBIOLÓGICO", tecnicas, key="k_tecnica", index=buscar_idx(tecnicas, m.get("Tecnica")), placeholder="Seleccione...")
            
            res_opciones = ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"]
            resultado_sel = st.radio("RESULTADO", res_opciones, key="k_res", index=buscar_idx(res_opciones, m.get("Resultado")))

            if resultado_sel == "CON DESARROLLO/ POSITIVO":
                microorganismos = sorted(["Absidia spp", "Achromobacter denitrificans", "Achromobacter sp.", "Achromobacter xylosoxidans", "Acinetobacter baumannii", "Acinetobacter baumanni complex", "Acinetobacter calcoaceticus", "Acinetobacter haemolyticus", "Acinetobacter johnsonii", "Acinetobacter junii", "Acinetobacter Iwoffi", "Acinetobacter nosocomialis", "Acinetobacter pittil", "Acinetobacter sp.", "Actinomyces israelii", "Actinomyces meyeri", "Actinomyces naelundii", "Actinomyces odontolyticus", "Actinomyces sp.", "Actinomyces viscosus", "Adenovirus 1", "Aeromonas bestirarum", "Aeromonas caviae", "Aeromonas caviae complex", "Aeromonas hydrophila", "Aeromonas salmonicida", "Aeromonas sp.", "Aeromonas veroni", "Alcaligenes faecalis", "Alcaligenes sp.", "Aspergillus flavus", "Aspergillus fumigatus", "Aspergillus spp.", "Bacillus anthracis", "Bacillus cereus", "Bacillus circulans", "Bacillus sp.", "Bacillus sp., no anthracis", "Bacillus sp., no cereus", "Bacillus subtilis", "Bacillus subtilis sp. complex", "Bacteroides bivius [Prevotella bivia]", "Bacteroides caccae", "Bacteroides distasonis", "Bacteroides eggerrthii", "Bacteroides fragilis", "Bacteroides fragilis group", "Bacteroides ovatus", "Bacteroides sp.", "Bacteroides spp.", "Brevundimonas diminuta", "Brevundimonas vesicularis", "Burkholderia cepacia", "Burkholderia cepacia complex", "Burkholderia gladioli", "Burkholderia sp.", "Candida albicans", "Candida auris", "Candida glabrata", "Candida guilliermondii", "Candida krusei", "Candida lusitaniae", "Candida parapsilosis", "Candida spp", "Candida tropicalis", "Cardiobacterium hominis", "Cardiobacterium sp.", "Chromobacterium violaceum", "Chryseobacterium gleum", "Chryseobacterium indologenes", "Chryseobacterium sp.", "Chryseomonas luteola", "Chryseomonas sp.", "Citrobacter amalonaticus", "Citrobacter braakii", "Citrobacter farmeri", "Citrobacter freundii", "Citrobacter koseri", "Citrobacter sedlakii", "Citrobacter sp.", "Citrobacter wekmanii", "Citrobacter youngae", "Clostridioides difficile", "Comamonas terrigena", "Comamonas testosteroni", "Corynebacterium amycolatum", "Corynebacterium jeikeium", "Corynebacterium sp.", "Corynebacterium striatum", "Corynebacterium urealyticum", "Corynebacterium xerosis", "Coxsackie", "Cronobacter sakazakii", "Cronobacter sp.", "Cryptococcus albidus", "Cryptococcus gattii", "Cryptococcus laurentii", "Cryptococcus spp.", "Cryptosporidium spp.", "Cutibacterium acnes", "Cutibacterium avidum", "Cutibacterium granulosum", "Cutibacterium sp.", "Cyclospora cayetanensis", "Delftia acidovorans", "Delftia sp.", "Edwardsiella sp.", "Edwardsiella tarda", "Elizabethkingia meningoseptica", "Elizabethkingia sp.", "Empedobacter brevis", "Enterobacter aerogenes", "Enterobacter amnigenus", "Enterobacter asburiae", "Enterobacter bugandensis", "Enterobacter cancerogenus", "Enterobacter cloacae", "Enterobacter cloacae complex", "Enterobacter gergoviae", "Enterobacter hormaechei", "Enterobacter kobei", "Enterobacter ludwigi", "Enterobacter sp.", "Enterobius vermicularis", "Enterococcus avium", "Enterococcus casseliflavus", "Enterococcus durans", "Enterococcus faecalis", "Enterococcus faecium", "Enterococcus flavescens", "Enterococcus gallinarum", "Enterococcus hirae", "Enterococcus malodoratus", "Enterococcus mundtiii", "Enterococcus raffinosus", "Enterococcus sacharolyticus", "Enterococcus sp.", "Enterovirus", "Erysipelothrix rhusiopathiae", "Erysipelothrix sp.", "Escherichia coli", "Escherichia coli, serogroup 0157", "Fusarium spp.", "Giardia spp.", "Hafnia alvei", "Hafnia sp.", "Hepatitis A", "Hepatitis B", "Hepatitis C", "Influenza A", "Influenza AH1N1", "Influenza AH3N2", "Influenza B", "Influenza virus", "Klebsiella aerogenes", "Klebsiella oxytoca", "Klebsiella ozaenae", "Klebsiella pneumoniae", "Klebsiella sp.", "Klebsiella varicola", "Kluyvera ascorbata", "Kocuria kristinae", "Kocuria rosea", "Kocuria sp.", "Leclercia adecarboxylata", "Lichteimia spp.", "Malassezia spp.", "Moraxella bovis", "Moraxella lacunata", "Moraxella nonliquefaciens", "Moraxella osloensis", "Moraxella sp.", "Morganella morganii", "Morganella sp.", "Mucor spp.", "Mycobacterium abscessus", "Mycobacterium avium-intracellulare", "Mycobacterium chelonae", "Mycobacterium fortuitum", "Mycobacterium mucogenicum", "Norovirus", "Ochrobactrum anthropi", "Otros", "Pantoea agglomerans", "Pantoea sp.", "Pediculus humanus capitis", "Pediculus humanus corporis", "Peptostreptococcus anaerobius", "Peptostreptococcus russellii", "Peptostreptococcus sp.", "Peptostreptococcus stomatis", "Prevotella oralis", "Prevotella bivia", "Prevotella denticola", "Prevotella disiens", "Prevotella intermedia", "Prevotella loescheii", "Prevotella melaninogenica", "Prevotella sp.", "Proteus hauseri", "Proteus mirabilis", "Proteus penneri", "Proteus sp.", "Proteus vulgaris", "Providencia alcalifaciens", "Providencia rettgeri", "Providencia rustigianii", "Providencia sp.", "Providencia stuartii", "Pseudomonas aeruginosa", "Pseudomonas alcaligenes", "Pseudomonas fluorescens", "Pseudomonas luteola", "Pseudomonas mendocina", "Pseudomonas monteilii", "Pseudomonas putida", "Pseudomonas sp.", "Pseudomonas stutzeri", "Ralstonia ornithinolytica", "Ralstonia pickettii", "Ralstonia sp.", "Raoultella ornithinolytica", "Raoultella planticola", "Rhinovirus", "Rhizobium radiobacter", "Rhizopus spp.", "Rhodotorula spp.", "Rotavirus", "Rubeola", "Saccharomyces cerevisiae", "Salmonella arizona", "Salmonella choleraesuis", "Salmonella enteritidis", "Salmonella paratyphi", "Salmonella sp.", "Salmonella typhi", "Sarampion", "Sarcoptes scabiei", "SARS-COV-2", "Serratia fonticola", "Serratia liquefaciens", "Serratia marcescens", "Serratia odorifera", "Serratia plymuthica", "Serratia rubidaea", "Serratia Sp.", "Shewanella prutrefaciens", "Shigella boydii", "Shigella dysenteriae", "Shigella flexneri", "Shigella sonnei", "Shigella sp.", "Sphingomonas paucimobilis", "Staphylococcus aureus", "Staphylococcus auricularis", "Staphylococcus capitis", "Staphylococcus coagulasa negativo", "Staphylococcus cohnii", "Staphylococcus epidermidis", "Staphylococcus haemolyticus", "Staphylococcus hominis", "Staphylococcus hyicus", "Staphylococcus intermedius", "Staphylococcus kloosii", "Staphylococcus lentus", "Staphylococcus lugdunensis", "Staphylococcus pseudointermedius", "Staphylococcus saccharolyticus", "Staphylococcus saprophyticus", "Staphylococcus schleiferi", "Staphylococcus sciuri", "Staphylococcus simulans", "Staphylococcus Sp.", "Staphylococcus warneri", "Staphylococcus xylosus", "Stenotrophomonas maltophilia", "Streptococcus agalactiae", "Streptococcus alactolyticus", "Streptococcus anginosus", "Streptococcus bovis group", "Streptococcus constellatus", "Streptococcus mitis", "Streptococcus spp.", "Streptococcus thoraltensis", "Streptococcus viridans", "Trichosporon asahii", "Varicela Zoster", "Vibrio alginolyticus", "Vibrio cholerae", "Vibrio fluvialis", "Vibrio parahaelolyticus", "Vibrio sp.", "Vibrio vulnificus", "Virus de Inmunodeficiencia Humana", "Virus sincitial respiratorio"])
                micro_sel = st.selectbox("MICROORGANISMO AISLADO", microorganismos, key="k_micro", index=buscar_idx(microorganismos, m.get("MicroOrg")), placeholder="Seleccione...")

                # --- CAMPO CONDICIONAL SI ES "OTROS" ---
                if str(micro_sel).strip().upper() == "OTROS":
                    otro_micro_val = st.text_input(
                        "Especifique el microorganismo:", 
                        key="k_otro_micro", 
                        value=m.get("Otro_MicroOrg", ""),
                        placeholder="Ej. Elizabethkingia anophelis..."
                    )

                # --- SUSCEPTIBILIDAD ---
                st.subheader("Prueba de Susceptibilidad")
                susp_sel = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD?", ["No", "Sí"], key="k_susp", index=buscar_idx(["No", "Sí"], m.get("Susp", "No")), horizontal=True)
                
                if susp_sel == "Sí":
                    opciones_tecnica_susp = ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"]
                    tecnica_susp_sel = st.selectbox(
                        "TÉCNICA PARA SUSCEPTIBILIDAD", 
                        opciones_tecnica_susp, 
                        key="k_tecnica_susp", 
                        index=buscar_idx(opciones_tecnica_susp, m.get("Tecnica_Susp")),
                        placeholder="Seleccione la técnica..."
                    )
                    
                    # --- SEPARACIÓN VISUAL ENTRE PRUEBA Y TABLA ---
                    st.divider()
                    st.subheader("Tabla de Antimicrobianos")
                    st.caption("Seleccione los antimicrobianos probados e ingrese la interpretación y CMI correspondiente.")
                    st.write("")

                    c1, c2, c3, c4 = st.columns([0.5, 2, 2, 1])
                    c1.write("**Sel**"); c2.write("**ANTIMICROBIANO**"); c3.write("**S / I / R / ND**"); c4.write("**CMI**")
                    
                    for ab in antibioticos_master:
                        check_key = f"check_{ab}"
                        is_selected = st.session_state.get(check_key, m.get(check_key, False))
                        row_class = "highlight-row" if is_selected else ""
                        
                        with st.container():
                            st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)
                            cols = st.columns([0.5, 2, 2, 1])
                            new_state = cols[0].checkbox("", key=check_key, value=is_selected)
                            cols[1].markdown(f"**{ab}**")
                            
                            if new_state:
                                res_key = f"res_{ab}"
                                cmi_key = f"cmi_{ab}"
                                
                                val_res = st.session_state.get(res_key, m.get(res_key, "ND"))
                                radio_res = cols[2].radio(
                                    f"Res_{ab}", 
                                    ["S", "I", "R", "ND"], 
                                    key=res_key, 
                                    index=buscar_idx(["S", "I", "R", "ND"], val_res), 
                                    horizontal=True, 
                                    label_visibility="collapsed"
                                )
                                cols[3].text_input(
                                    f"CMI_{ab}", 
                                    key=cmi_key, 
                                    value=m.get(cmi_key, ""), 
                                    label_visibility="collapsed", 
                                    placeholder="CMI", 
                                    disabled=(radio_res == "ND")
                                )
                            st.markdown('</div>', unsafe_allow_html=True)

    # --- FUNCIÓN DE GUARDADO CENTRALIZADA Y SEGURA ---
    def guardar():
        def clean_val(val):
            return str(val).upper().strip() if val else ""

        is_hemo = st.session_state.get("k_hemo_its", "No") == "Sí"
        is_tomo = st.session_state.get("k_tomo_muestra", "No") == "Sí"
        is_pos = is_tomo and (st.session_state.get("k_res") == "CON DESARROLLO/ POSITIVO")
        is_susp = is_pos and (st.session_state.get("k_susp") == "Sí")

        data = {
            "Hemo_ITS": clean_val(st.session_state.get("k_hemo_its")), 
            "sp": clean_val(st.session_state.get("sp")) if is_hemo else "NO",
            "scc": clean_val(st.session_state.get("scc")) if is_hemo else "NO", 
            "pcc": clean_val(st.session_state.get("pcc")) if is_hemo else "NO",
            "Tomada": clean_val(st.session_state.get("k_tomo_muestra")), 
            "Fecha_Toma": st.session_state.get("k_f_toma") if is_tomo else None,
            "Fecha_Res": st.session_state.get("k_f_res") if is_tomo else None,
            "Lab": clean_val(st.session_state.get("k_lab")) if is_tomo else "", 
            "Muestra": clean_val(st.session_state.get("k_muestra")) if is_tomo else "", 
            "Tecnica": clean_val(st.session_state.get("k_tecnica")) if is_tomo else "",
            "Resultado": clean_val(st.session_state.get("k_res")) if is_tomo else "",
            "MicroOrg": clean_val(micro_sel) if is_pos else "",
            "Otro_MicroOrg": clean_val(otro_micro_val) if (is_pos and str(micro_sel).strip().upper() == "OTROS") else "",
            "Susp": clean_val(st.session_state.get("k_susp")) if is_pos else "NO",
            "Tecnica_Susp": clean_val(tecnica_susp_sel) if is_susp else ""
        }
        
        for ab in antibioticos_master:
            if is_susp:
                data[f"check_{ab}"] = st.session_state.get(f"check_{ab}", False)
                data[f"res_{ab}"] = clean_val(st.session_state.get(f"res_{ab}", "ND"))
                data[f"cmi_{ab}"] = str(st.session_state.get(f"cmi_{ab}", "")).strip()
            else:
                data[f"check_{ab}"] = False
                data[f"res_{ab}"] = "ND"
                data[f"cmi_{ab}"] = ""

        st.session_state.datos_completos["Micro"] = data

    # --- NAVEGACIÓN ---
    st.divider()
    c_atras, c_adelante = st.columns([1, 4])
    if c_atras.button("⬅️ Atrás"): 
        guardar()
        st.session_state.pagina_actual = ORDEN[ORDEN.index(st.session_state.pagina_actual) - 1]
        st.rerun()
    if c_adelante.button("💾 Guardar y continuar"): 
        guardar()
        st.session_state.pagina_actual = ORDEN[ORDEN.index(st.session_state.pagina_actual) + 1]
        st.rerun()

if __name__ == "__main__":
    render()
