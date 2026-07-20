import streamlit as st
from config import ORDEN

def render():
    st.title("Infección Polimicrobiana")

    # --- 0. RECUPERACIÓN DE ESTADOS ---
    if "datos_completos" not in st.session_state:
        st.session_state.datos_completos = {}

    p = st.session_state.datos_completos.get("Polimicrobiana", {})

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

    # --- 1. SELECCIÓN DE POLIMICROBIANA ---
    with st.container(border=True):
        es_polimicrobiana = st.radio(
            "¿SE TRATA DE UNA INFECCIÓN POLIMICROBIANA?", 
            ["No", "Sí"], 
            key="k_es_poli", 
            index=buscar_idx(["No", "Sí"], p.get("Es_Polimicrobiana", "No")), 
            horizontal=True
        )

        micro_sel, otro_micro_val, susp_sel, tecnica_susp_sel = "", "", "No", ""

        if es_polimicrobiana == "Sí":
            st.subheader("Datos del Microorganismo Adicional")
            
            microorganismos = sorted(["Absidia spp", "Achromobacter denitrificans", "Achromobacter sp.", "Achromobacter xylosoxidans", "Acinetobacter baumannii", "Acinetobacter baumanni complex", "Acinetobacter calcoaceticus", "Acinetobacter haemolyticus", "Acinetobacter johnsonii", "Acinetobacter junii", "Acinetobacter Iwoffi", "Acinetobacter nosocomialis", "Acinetobacter pittil", "Acinetobacter sp.", "Actinomyces israelii", "Actinomyces meyeri", "Actinomyces naelundii", "Actinomyces odontolyticus", "Actinomyces sp.", "Actinomyces viscosus", "Adenovirus 1", "Aeromonas bestirarum", "Aeromonas caviae", "Aeromonas caviae complex", "Aeromonas hydrophila", "Aeromonas salmonicida", "Aeromonas sp.", "Aeromonas veroni", "Alcaligenes faecalis", "Alcaligenes sp.", "Aspergillus flavus", "Aspergillus fumigatus", "Aspergillus spp.", "Bacillus anthracis", "Bacillus cereus", "Bacillus circulans", "Bacillus sp.", "Bacillus sp., no anthracis", "Bacillus sp., no cereus", "Bacillus subtilis", "Bacillus subtilis sp. complex", "Bacteroides bivius [Prevotella bivia]", "Bacteroides caccae", "Bacteroides distasonis", "Bacteroides eggerrthii", "Bacteroides fragilis", "Bacteroides fragilis group", "Bacteroides ovatus", "Bacteroides sp.", "Bacteroides spp.", "Brevundimonas diminuta", "Brevundimonas vesicularis", "Burkholderia cepacia", "Burkholderia cepacia complex", "Burkholderia gladioli", "Burkholderia sp.", "Candida albicans", "Candida auris", "Candida glabrata", "Candida guilliermondii", "Candida krusei", "Candida lusitaniae", "Candida parapsilosis", "Candida spp", "Candida tropicalis", "Cardiobacterium hominis", "Cardiobacterium sp.", "Chromobacterium violaceum", "Chryseobacterium gleum", "Chryseobacterium indologenes", "Chryseobacterium sp.", "Chryseomonas luteola", "Chryseomonas sp.", "Citrobacter amalonaticus", "Citrobacter braakii", "Citrobacter farmeri", "Citrobacter freundii", "Citrobacter koseri", "Citrobacter sedlakii", "Citrobacter sp.", "Citrobacter wekmanii", "Citrobacter youngae", "Clostridioides difficile", "Comamonas terrigena", "Comamonas testosteroni", "Corynebacterium amycolatum", "Corynebacterium jeikeium", "Corynebacterium sp.", "Corynebacterium striatum", "Corynebacterium urealyticum", "Corynebacterium xerosis", "Coxsackie", "Cronobacter sakazakii", "Cronobacter sp.", "Cryptococcus albidus", "Cryptococcus gattii", "Cryptococcus laurentii", "Cryptococcus spp.", "Cryptosporidium spp.", "Cutibacterium acnes", "Cutibacterium avidum", "Cutibacterium granulosum", "Cutibacterium sp.", "Cyclospora cayetanensis", "Delftia acidovorans", "Delftia sp.", "Edwardsiella sp.", "Edwardsiella tarda", "Elizabethkingia meningoseptica", "Elizabethkingia sp.", "Empedobacter brevis", "Enterobacter aerogenes", "Enterobacter amnigenus", "Enterobacter asburiae", "Enterobacter bugandensis", "Enterobacter cancerogenus", "Enterobacter cloacae", "Enterobacter cloacae complex", "Enterobacter gergoviae", "Enterobacter hormaechei", "Enterobacter kobei", "Enterobacter ludwigi", "Enterobacter sp.", "Enterobius vermicularis", "Enterococcus avium", "Enterococcus casseliflavus", "Enterococcus durans", "Enterococcus faecalis", "Enterococcus faecium", "Enterococcus flavescens", "Enterococcus gallinarum", "Enterococcus hirae", "Enterococcus malodoratus", "Enterococcus mundtiii", "Enterococcus raffinosus", "Enterococcus sacharolyticus", "Enterococcus sp.", "Enterovirus", "Erysipelothrix rhusiopathiae", "Erysipelothrix sp.", "Escherichia coli", "Escherichia coli, serogroup 0157", "Fusarium spp.", "Giardia spp.", "Hafnia alvei", "Hafnia sp.", "Hepatitis A", "Hepatitis B", "Hepatitis C", "Influenza A", "Influenza AH1N1", "Influenza AH3N2", "Influenza B", "Influenza virus", "Klebsiella aerogenes", "Klebsiella oxytoca", "Klebsiella ozaenae", "Klebsiella pneumoniae", "Klebsiella sp.", "Klebsiella varicola", "Kluyvera ascorbata", "Kocuria kristinae", "Kocuria rosea", "Kocuria sp.", "Leclercia adecarboxylata", "Lichteimia spp.", "Malassezia spp.", "Moraxella bovis", "Moraxella lacunata", "Moraxella nonliquefaciens", "Moraxella osloensis", "Moraxella sp.", "Morganella morganii", "Morganella sp.", "Mucor spp.", "Mycobacterium abscessus", "Mycobacterium avium-intracellulare", "Mycobacterium chelonae", "Mycobacterium fortuitum", "Mycobacterium mucogenicum", "Norovirus", "Ochrobactrum anthropi", "Otros", "Pantoea agglomerans", "Pantoea sp.", "Pediculus humanus capitis", "Pediculus humanus corporis", "Peptostreptococcus anaerobius", "Peptostreptococcus russellii", "Peptostreptococcus sp.", "Peptostreptococcus stomatis", "Prevotella oralis", "Prevotella bivia", "Prevotella denticola", "Prevotella disiens", "Prevotella intermedia", "Prevotella loescheii", "Prevotella melaninogenica", "Prevotella sp.", "Proteus hauseri", "Proteus mirabilis", "Proteus penneri", "Proteus sp.", "Proteus vulgaris", "Providencia alcalifaciens", "Providencia rettgeri", "Providencia rustigianii", "Providencia sp.", "Providencia stuartii", "Pseudomonas aeruginosa", "Pseudomonas alcaligenes", "Pseudomonas fluorescens", "Pseudomonas luteola", "Pseudomonas mendocina", "Pseudomonas monteilii", "Pseudomonas putida", "Pseudomonas sp.", "Pseudomonas stutzeri", "Ralstonia ornithinolytica", "Ralstonia pickettii", "Ralstonia sp.", "Raoultella ornithinolytica", "Raoultella planticola", "Rhinovirus", "Rhizobium radiobacter", "Rhizopus spp.", "Rhodotorula spp.", "Rotavirus", "Rubeola", "Saccharomyces cerevisiae", "Salmonella arizona", "Salmonella choleraesuis", "Salmonella enteritidis", "Salmonella paratyphi", "Salmonella sp.", "Salmonella typhi", "Sarampion", "Sarcoptes scabiei", "SARS-COV-2", "Serratia fonticola", "Serratia liquefaciens", "Serratia marcescens", "Serratia odorifera", "Serratia plymuthica", "Serratia rubidaea", "Serratia Sp.", "Shewanella prutrefaciens", "Shigella boydii", "Shigella dysenteriae", "Shigella flexneri", "Shigella sonnei", "Shigella sp.", "Sphingomonas paucimobilis", "Staphylococcus aureus", "Staphylococcus auricularis", "Staphylococcus capitis", "Staphylococcus coagulasa negativo", "Staphylococcus cohnii", "Staphylococcus epidermidis", "Staphylococcus haemolyticus", "Staphylococcus hominis", "Staphylococcus hyicus", "Staphylococcus intermedius", "Staphylococcus kloosii", "Staphylococcus lentus", "Staphylococcus lugdunensis", "Staphylococcus pseudointermedius", "Staphylococcus saccharolyticus", "Staphylococcus saprophyticus", "Staphylococcus schleiferi", "Staphylococcus sciuri", "Staphylococcus simulans", "Staphylococcus Sp.", "Staphylococcus warneri", "Staphylococcus xylosus", "Stenotrophomonas maltophilia", "Streptococcus agalactiae", "Streptococcus alactolyticus", "Streptococcus anginosus", "Streptococcus bovis group", "Streptococcus constellatus", "Streptococcus mitis", "Streptococcus spp.", "Streptococcus thoraltensis", "Streptococcus viridans", "Trichosporon asahii", "Varicela Zoster", "Vibrio alginolyticus", "Vibrio cholerae", "Vibrio fluvialis", "Vibrio parahaemolyticus", "Vibrio sp.", "Vibrio vulnificus", "Virus de Inmunodeficiencia Humana", "Virus sincitial respiratorio"])
            micro_sel = st.selectbox("MICROORGANISMO AISLADO", microorganismos, key="k_poli_micro", index=buscar_idx(microorganismos, p.get("MicroOrg")), placeholder="Seleccione...")

            # --- CAMPO CONDICIONAL SI ES "OTROS" ---
            if str(micro_sel).strip().upper() == "OTROS":
                otro_micro_val = st.text_input(
                    "Especifique el microorganismo adicional:", 
                    key="k_poli_otro_micro", 
                    value=p.get("Otro_MicroOrg", ""),
                    placeholder="Ej. Elizabethkingia anophelis..."
                )

            # --- 2. SUSCEPTIBILIDAD ---
            st.subheader("Prueba de Susceptibilidad")
            susp_sel = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD ANTIMICROBIANA?", ["No", "Sí"], key="k_poli_susp", index=buscar_idx(["No", "Sí"], p.get("Susp", "No")), horizontal=True)
            
            if susp_sel == "Sí":
                opciones_tecnica_susp = ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"]
                tecnica_susp_sel = st.selectbox(
                    "TÉCNICA PARA SUSCEPTIBILIDAD", 
                    opciones_tecnica_susp, 
                    key="k_poli_tecnica_susp", 
                    index=buscar_idx(opciones_tecnica_susp, p.get("Tecnica_Susp")),
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
                    check_key = f"poli_check_{ab}"
                    is_selected = st.session_state.get(check_key, p.get(check_key, False))
                    row_class = "highlight-row" if is_selected else ""
                    
                    with st.container():
                        st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)
                        cols = st.columns([0.5, 2, 2, 1])
                        new_state = cols[0].checkbox("", key=check_key, value=is_selected)
                        cols[1].markdown(f"**{ab}**")
                        
                        if new_state:
                            res_key = f"poli_res_{ab}"
                            cmi_key = f"poli_cmi_{ab}"
                            
                            val_res = st.session_state.get(res_key, p.get(res_key, "ND"))
                            radio_res = cols[2].radio(
                                f"Poli_Res_{ab}", 
                                ["S", "I", "R", "ND"], 
                                key=res_key, 
                                index=buscar_idx(["S", "I", "R", "ND"], val_res), 
                                horizontal=True, 
                                label_visibility="collapsed"
                            )
                            cols[3].text_input(
                                f"Poli_CMI_{ab}", 
                                key=cmi_key, 
                                value=p.get(cmi_key, ""), 
                                label_visibility="collapsed", 
                                placeholder="CMI", 
                                disabled=(radio_res == "ND")
                            )
                        st.markdown('</div>', unsafe_allow_html=True)

    # --- FUNCIÓN DE GUARDADO CENTRALIZADA Y SEGURA ---
    def guardar():
        def clean_val(val):
            return str(val).upper().strip() if val else ""

        is_poli = st.session_state.get("k_es_poli", "No") == "Sí"
        is_susp = is_poli and (st.session_state.get("k_poli_susp") == "Sí")

        data = {
            "Es_Polimicrobiana": clean_val(st.session_state.get("k_es_poli")), 
            "MicroOrg": clean_val(micro_sel) if is_poli else "",
            "Otro_MicroOrg": clean_val(otro_micro_val) if (is_poli and str(micro_sel).strip().upper() == "OTROS") else "",
            "Susp": clean_val(st.session_state.get("k_poli_susp")) if is_poli else "NO",
            "Tecnica_Susp": clean_val(tecnica_susp_sel) if is_susp else ""
        }
        
        for ab in antibioticos_master:
            if is_susp:
                data[f"poli_check_{ab}"] = st.session_state.get(f"poli_check_{ab}", False)
                data[f"poli_res_{ab}"] = clean_val(st.session_state.get(f"poli_res_{ab}", "ND"))
                data[f"poli_cmi_{ab}"] = str(st.session_state.get(f"poli_cmi_{ab}", "")).strip()
            else:
                data[f"poli_check_{ab}"] = False
                data[f"poli_res_{ab}"] = "ND"
                data[f"poli_cmi_{ab}"] = ""

        st.session_state.datos_completos["Polimicrobiana"] = data

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
