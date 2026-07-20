import streamlit as st
from config import ORDEN

def render():
    st.set_page_config(layout="wide")
    st.title("Diagnóstico Microbiológico")

    # --- 0. RECUPERACIÓN DE ESTADOS ---
    m = st.session_state.datos_completos.get("Micro", {})
    
    # Se eliminó la validación que inhabilitaba los campos basada en 'tipo_deteccion'

    # --- CSS PARA EL SOMBREADO ---
    st.markdown("""
        <style>
        .highlight-row { 
            background-color: #e6f3ff !important; 
            padding: 10px; 
            border-radius: 8px; 
            margin-bottom: 5px; 
            border: 1px solid #d1e7fd; 
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. HEMOCULTIVOS ---
    hemocultivo_its = st.radio("¿Se tomaron hemocultivos para ITS?", ["No", "Sí"], key="k_hemo_its", index=["No", "Sí"].index(m.get("Hemo_ITS", "No")), horizontal=True)
    
    if hemocultivo_its == "Sí":
        c_hem1, c_hem2, c_hem3 = st.columns(3)
        c_hem1.radio("SANGRE PERIFÉRICA", ["No", "Sí"], key="sp", index=["No", "Sí"].index(m.get("sp", "No")), horizontal=True)
        c_hem2.radio("SANGRE POR CATETÉR CENTRAL", ["No", "Sí"], key="scc", index=["No", "Sí"].index(m.get("scc", "No")), horizontal=True)
        c_hem3.radio("PUNTA DE CATETÉR CENTRAL", ["No", "Sí"], key="pcc", index=["No", "Sí"].index(m.get("pcc", "No")), horizontal=True)

    # --- 2. PREGUNTA GENERAL ---
    se_tomo_muestra = st.radio("¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", ["No", "Sí"], key="k_tomo_muestra", index=["No", "Sí"].index(m.get("Tomada", "No")), horizontal=True)

    if (se_tomo_muestra == "Sí" or hemocultivo_its == "Sí"):
        c1, c2 = st.columns(2)
        with c1:
            st.date_input("FECHA DE TOMA", key="k_f_toma", value=m.get("Fecha_Toma") or None, format="DD/MM/YYYY")
            lab_opciones = ["De la unidad", "InDRE", "LESP", "LAVE", "PRIVADO/SUBROGADO", "OTRO"]
            st.selectbox("LABORATORIO", lab_opciones, key="k_lab", index=lab_opciones.index(m.get("Lab")) if m.get("Lab") in lab_opciones else None, placeholder="Seleccione...")
        with c2:
            st.date_input("FECHA DE RESULTADO", key="k_f_res", value=m.get("Fecha_Res") or None, format="DD/MM/YYYY")
            muestras_opciones = ["Orina de chorro medio", "Orina por puncion suprapubica", "Orina cateter vesical", "Sonda de entrada por salida", "Aspirado bronquial", "Aspirado traqueal", "Esputo inducido", "Esputo espontaneo", "Lavado bronco alveolar", "Biopsia transbronquial", "Biopsia pulmonar", "Biopsia pleural", "Sangre periferica", "Aspirado", "Biopsia", "Exudado faringeo", "Drenaje otico", "Sangre por cateter central", "Punta de cateter central", "Drenaje", "Liquido pericardico", "Heces", "Aspirado de absceso o secrecion de herida", "Hisopado de herida quirurgica +score Q", "Liquidos organicos", "Biopsia cuantitativa", "Aspirado de absceso", "Hisopado + score Q", "Liquido sinovial", "Sonicado de piezas protesicas para cultivo", "Hisopado conjuntival", "Raspado ocular", "Aspirado de humor vitreo", "Aspirado de humor acuoso", "Lavado ocular", "Liquido cefaloraquideo", "Liquido peritoneal", "Otro"]
            st.selectbox("TIPO DE MUESTRA", muestras_opciones, key="k_muestra", index=muestras_opciones.index(m.get("Muestra")) if m.get("Muestra") in muestras_opciones else None, placeholder="Seleccione...")

        tecnicas = ["Bioquímicas manuales", "Inmunocromatografía", "Manuales API", "Semi-automatizados (AutoScan)", "VITEK (automatizada)", "MicroScan (automatizada)", "Aries Sensititre (automatizada)", "Phoenix (automatizada)", "Espectrometría de masas. MALDI-TOF", "PCR (moleculares)", "Sondas de hibridación (moleculares)"]
        st.selectbox("TÉCNICA PARA DIAGNÓSTICO MICROBIOLÓGICO", tecnicas, key="k_tecnica", index=tecnicas.index(m.get("Tecnica")) if m.get("Tecnica") in tecnicas else None, placeholder="Seleccione...")
        
        resultado = st.radio("RESULTADO", ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"], key="k_res", index=["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"].index(m.get("Resultado")) if m.get("Resultado") in ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"] else None)

        if resultado == "CON DESARROLLO/ POSITIVO":
            microorganismos = sorted(["Absidia spp", "Achromobacter denitrificans", "Achromobacter sp.", "Achromobacter xylosoxidans", "Acinetobacter baumannii", "Acinetobacter baumanni complex", "Acinetobacter calcoaceticus", "Acinetobacter haemolyticus", "Acinetobacter johnsonii", "Acinetobacter junii", "Acinetobacter Iwoffi", "Acinetobacter nosocomialis", "Acinetobacter pittil", "Acinetobacter sp.", "Actinomyces israelii", "Actinomyces meyeri", "Actinomyces naelundii", "Actinomyces odontolyticus", "Actinomyces sp.", "Actinomyces viscosus", "Adenovirus 1", "Aeromonas bestirarum", "Aeromonas caviae", "Aeromonas caviae complex", "Aeromonas hydrophila", "Aeromonas salmonicida", "Aeromonas sp.", "Aeromonas veroni", "Alcaligenes faecalis", "Alcaligenes sp.", "Aspergillus flavus", "Aspergillus fumigatus", "Aspergillus spp.", "Bacillus anthracis", "Bacillus cereus", "Bacillus circulans", "Bacillus sp.", "Bacillus sp., no anthracis", "Bacillus sp., no cereus", "Bacillus subtilis", "Bacillus subtilis sp. complex", "Bacteroides bivius [Prevotella bivia]", "Bacteroides caccae", "Bacteroides distasonis", "Bacteroides eggerrthii", "Bacteroides fragilis", "Bacteroides fragilis group", "Bacteroides ovatus", "Bacteroides sp.", "Bacteroides spp.", "Brevundimonas diminuta", "Brevundimonas vesicularis", "Burkholderia cepacia", "Burkholderia cepacia complex", "Burkholderia gladioli", "Burkholderia sp.", "Candida albicans", "Candida auris", "Candida glabrata", "Candida guilliermondii", "Candida krusei", "Candida lusitaniae", "Candida parapsilosis", "Candida spp", "Candida tropicalis", "Cardiobacterium hominis", "Cardiobacterium sp.", "Chromobacterium violaceum", "Chryseobacterium gleum", "Chryseobacterium indologenes", "Chryseobacterium sp.", "Chryseomonas luteola", "Chryseomonas sp.", "Citrobacter amalonaticus", "Citrobacter braakii", "Citrobacter farmeri", "Citrobacter freundii", "Citrobacter koseri", "Citrobacter sedlakii", "Citrobacter sp.", "Citrobacter wekmanii", "Citrobacter youngae", "Clostridioides difficile", "Comamonas terrigena", "Comamonas testosteroni", "Corynebacterium amycolatum", "Corynebacterium jeikeium", "Corynebacterium sp.", "Corynebacterium striatum", "Corynebacterium urealyticum", "Corynebacterium xerosis", "Coxsackie", "Cronobacter sakazakii", "Cronobacter sp.", "Cryptococcus albidus", "Cryptococcus gattii", "Cryptococcus laurentii", "Cryptococcus spp.", "Cryptosporidium spp.", "Cutibacterium acnes", "Cutibacterium avidum", "Cutibacterium granulosum", "Cutibacterium sp.", "Cyclospora cayetanensis", "Delftia acidovorans", "Delftia sp.", "Edwardsiella sp.", "Edwardsiella tarda", "Elizabethkingia meningoseptica", "Elizabethkingia sp.", "Empedobacter brevis", "Enterobacter aerogenes", "Enterobacter amnigenus", "Enterobacter asburiae", "Enterobacter bugandensis", "Enterobacter cancerogenus", "Enterobacter cloacae", "Enterobacter cloacae complex", "Enterobacter gergoviae", "Enterobacter hormaechei", "Enterobacter kobei", "Enterobacter ludwigi", "Enterobacter sp.", "Enterobius vermicularis", "Enterococcus avium", "Enterococcus casseliflavus", "Enterococcus durans", "Enterococcus faecalis", "Enterococcus faecium", "Enterococcus flavescens", "Enterococcus gallinarum", "Enterococcus hirae", "Enterococcus malodoratus", "Enterococcus mundtiii", "Enterococcus raffinosus", "Enterococcus sacharolyticus", "Enterococcus sp.", "Enterovirus", "Erysipelothrix rhusiopathiae", "Erysipelothrix sp.", "Escherichia coli", "Escherichia coli, serogroup 0157", "Fusarium spp.", "Giardia spp.", "Hafnia alvei", "Hafnia sp.", "Hepatitis A", "Hepatitis B", "Hepatitis C", "Influenza A", "Influenza AH1N1", "Influenza AH3N2", "Influenza B", "Influenza virus", "Klebsiella aerogenes", "Klebsiella oxytoca", "Klebsiella ozaenae", "Klebsiella pneumoniae", "Klebsiella sp.", "Klebsiella varicola", "Kluyvera ascorbata", "Kocuria kristinae", "Kocuria rosea", "Kocuria sp.", "Leclercia adecarboxylata", "Lichteimia spp.", "Malassezia spp.", "Moraxella bovis", "Moraxella lacunata", "Moraxella nonliquefaciens", "Moraxella osloensis", "Moraxella sp.", "Morganella morganii", "Morganella sp.", "Mucor spp.", "Mycobacterium abscessus", "Mycobacterium avium-intracellulare", "Mycobacterium chelonae", "Mycobacterium fortuitum", "Mycobacterium mucogenicum", "Norovirus", "Ochrobactrum anthropi", "Otros", "Pantoea agglomerans", "Pantoea sp.", "Pediculus humanus capitis", "Pediculus humanus corporis", "Peptostreptococcus anaerobius", "Peptostreptococcus russellii", "Peptostreptococcus sp.", "Peptostreptococcus stomatis", "Prevotella oralis", "Prevotella bivia", "Prevotella denticola", "Prevotella disiens", "Prevotella intermedia", "Prevotella loescheii", "Prevotella melaninogenica", "Prevotella sp.", "Proteus hauseri", "Proteus mirabilis", "Proteus penneri", "Proteus sp.", "Proteus vulgaris", "Providencia alcalifaciens", "Providencia rettgeri", "Providencia rustigianii", "Providencia sp.", "Providencia stuartii", "Pseudomonas aeruginosa", "Pseudomonas alcaligenes", "Pseudomonas fluorescens", "Pseudomonas luteola", "Pseudomonas mendocina", "Pseudomonas monteilii", "Pseudomonas putida", "Pseudomonas sp.", "Pseudomonas stutzeri", "Ralstonia ornithinolytica", "Ralstonia pickettii", "Ralstonia sp.", "Raoultella ornithinolytica", "Raoultella planticola", "Rhinovirus", "Rhizobium radiobacter", "Rhizopus spp.", "Rhodotorula spp.", "Rotavirus", "Rubeola", "Saccharomyces cerevisiae", "Salmonella arizona", "Salmonella choleraesuis", "Salmonella enteritidis", "Salmonella paratyphi", "Salmonella sp.", "Salmonella typhi", "Sarampion", "Sarcoptes scabiei", "SARS-COV-2", "Serratia fonticola", "Serratia liquefaciens", "Serratia marcescens", "Serratia odorifera", "Serratia plymuthica", "Serratia rubidaea", "Serratia Sp.", "Shewanella prutrefaciens", "Shigella boydii", "Shigella dysenteriae", "Shigella flexneri", "Shigella sonnei", "Shigella sp.", "Sphingomonas paucimobilis", "Staphylococcus aureus", "Staphylococcus auricularis", "Staphylococcus capitis", "Staphylococcus coagulasa negativo", "Staphylococcus cohnii", "Staphylococcus epidermidis", "Staphylococcus haemolyticus", "Staphylococcus hominis", "Staphylococcus hyicus", "Staphylococcus intermedius", "Staphylococcus kloosii", "Staphylococcus lentus", "Staphylococcus lugdunensis", "Staphylococcus pseudointermedius", "Staphylococcus saccharolyticus", "Staphylococcus saprophyticus", "Staphylococcus schleiferi", "Staphylococcus sciuri", "Staphylococcus simulans", "Staphylococcus Sp.", "Staphylococcus warneri", "Staphylococcus xylosus", "Stenotrophomonas maltophilia", "Streptococcus agalactiae", "Streptococcus alactolyticus", "Streptococcus anginosus", "Streptococcus bovis group", "Streptococcus constellatus", "Streptococcus mitis", "Streptococcus spp.", "Streptococcus thoraltensis", "Streptococcus viridans", "Trichosporon asahii", "Varicela Zoster", "Vibrio alginolyticus", "Vibrio cholerae", "Vibrio fluvialis", "Vibrio parahaelolyticus", "Vibrio sp.", "Vibrio vulnificus", "Virus de Inmunodeficiencia Humana", "Virus sincitial respiratorio"])
            st.selectbox("MICROORGANISMO AISLADO", microorganismos, key="k_micro", index=microorganismos.index(m.get("MicroOrg")) if m.get("MicroOrg") in microorganismos else None, placeholder="Seleccione...")

            # --- SUSCEPTIBILIDAD ---
            st.subheader("Prueba de Susceptibilidad")
            realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD?", ["No", "Sí"], key="k_susp", index=["No", "Sí"].index(m.get("Susp", "No")), horizontal=True)
            
            if realizo_susp == "Sí":
                antibioticos = ["AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", "AZTREONAM", "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA", "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANE-TAZOBACTAM", "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", "DAPTOMICINA", "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA", "IMIPENEM", "ITRACONAZOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "MICAFUNGINA", "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM", "POSACONAZOL", "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA", "TRIMETOPRIM-SULFAMETOXAZOL", "VANCOMICINA", "VORICONAZOL"]
                
                c1, c2, c3, c4 = st.columns([0.5, 2, 2, 1])
                c1.write("**Sel**"); c2.write("**ANTIMICROBIANO**"); c3.write("**S / I / R / ND**"); c4.write("**CMI**")
                
                for ab in antibioticos:
                    check_key = f"check_{ab}"
                    is_selected = st.session_state.get(check_key, m.get(check_key, False))
                    row_class = "highlight-row" if is_selected else ""
                    
                    with st.container():
                        st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)
                        cols = st.columns([0.5, 2, 2, 1])
                        new_state = cols[0].checkbox("", key=check_key, value=is_selected)
                        cols[1].markdown(f"**{ab}**")
                        if new_state:
                            res = cols[2].radio(f"Res_{ab}", ["S", "I", "R", "ND"], key=f"res_{ab}", index=["S", "I", "R", "ND"].index(m.get(f"res_{ab}", "ND")), horizontal=True, label_visibility="collapsed")
                            cols[3].text_input(f"CMI_{ab}", key=f"cmi_{ab}", value=m.get(f"cmi_{ab}", ""), label_visibility="collapsed", placeholder="CMI", disabled=(res == "ND"))
                        st.markdown('</div>', unsafe_allow_html=True)

    # --- GUARDADO ---
    def guardar():
        data = {
            "Hemo_ITS": st.session_state.get("k_hemo_its", "No"), "sp": st.session_state.get("sp", "No"),
            "scc": st.session_state.get("scc", "No"), "pcc": st.session_state.get("pcc", "No"),
            "Tomada": st.session_state.get("k_tomo_muestra", "No"), "Susp": st.session_state.get("k_susp", "No"),
            "MicroOrg": st.session_state.get("k_micro"), "Resultado": st.session_state.get("k_res"),
            "Fecha_Toma": st.session_state.get("k_f_toma"), "Fecha_Res": st.session_state.get("k_f_res"),
            "Lab": st.session_state.get("k_lab"), "Muestra": st.session_state.get("k_muestra"), "Tecnica": st.session_state.get("k_tecnica")
        }
        antibioticos = ["AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", "AZTREONAM", "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA", "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANE-TAZOBACTAM", "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", "DAPTOMICINA", "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA", "IMIPENEM", "ITRACONAZOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "MICAFUNGINA", "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM", "POSACONAZOL", "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA", "TRIMETOPRIM-SULFAMETOXAZOL", "VANCOMICINA", "VORICONAZOL"]
        for ab in antibioticos:
            data[f"check_{ab}"] = st.session_state.get(f"check_{ab}", False)
            data[f"res_{ab}"] = st.session_state.get(f"res_{ab}", "ND")
            data[f"cmi_{ab}"] = st.session_state.get(f"cmi_{ab}", "")
        st.session_state.datos_completos["Micro"] = data

    st.divider()
    c_atras, c_adelante = st.columns([1, 4])
    if c_atras.button("⬅️ Atrás"): guardar(); st.session_state.pagina_actual = ORDEN[ORDEN.index(st.session_state.pagina_actual) - 1]; st.rerun()
    if c_adelante.button("Guardar y continuar"): guardar(); st.session_state.pagina_actual = ORDEN[ORDEN.index(st.session_state.pagina_actual) + 1]; st.rerun()

if __name__ == "__main__":
    render()
