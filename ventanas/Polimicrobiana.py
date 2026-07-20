import streamlit as st
from config import ORDEN

def render():
    st.set_page_config(layout="wide")
    st.title("Infección Polimicrobiana")

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

    # --- 1. PERSISTENCIA: Recuperar datos guardados ---
    if "Polimicrobiana" not in st.session_state.datos_completos:
        st.session_state.datos_completos["Polimicrobiana"] = {}
    p = st.session_state.datos_completos["Polimicrobiana"]

    # --- 2. SELECCIÓN ---
    es_polimicrobiana = st.radio(
        "¿SE TRATA DE UNA INFECCIÓN POLIMICROBIANA?", ["No", "Sí"], 
        key="es_poli",
        index=["No", "Sí"].index(p.get("Es_Polimicrobiana", "No")), 
        horizontal=True
    )
    
    if es_polimicrobiana == "Sí":
        st.subheader("Datos del Microorganismo Adicional")
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

        # --- 3. SUSCEPTIBILIDAD ---
        st.subheader("Prueba de Susceptibilidad")
        st.caption("Selecciona la opción según corresponda: S=Susceptible. I= Intermedio. R= Resistente. ND= No determinada. *CMI= Concentración mínima inhibitoria.")
        
        realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD ANTIMICROBIANA?", ["No", "Sí"], horizontal=True)
        
        if realizo_susp == "Sí":
            st.selectbox("TÉCNICA PARA SUSCEPTIBILIDAD", ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"], index=None, placeholder="Seleccione...")
            
            antibioticos = ["AMIKACINA", "AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", "AZTREONAM", "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA", "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANE-TAZOBACTAM", "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", "DAPTOMICINA", "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA", "IMIPENEM", "ITRACONZAOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "MICAFUNGINA", "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM", "POSACONAZOL", "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA", "TRIMETOPRIM-SULFAMETOXAZOL", "VANCOMICINA", "VORICONAZOL"]
            
            c1, c2, c3, c4 = st.columns([0.5, 2, 2, 1])
            c1.write("**Sel**"); c2.write("**ANTIMICROBIANO**"); c3.write("**S / I / R / ND**"); c4.write("**CMI**")
            
            for ab in antibioticos:
                key_check = f"check_{ab}"
                is_selected = st.session_state.get(key_check, False)
                row_class = "highlight-row" if is_selected else ""
                
                with st.container():
                    st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)
                    cols = st.columns([0.5, 2, 2, 1])
                    new_state = cols[0].checkbox("", key=key_check)
                    cols[1].markdown(f"**{ab}**")
                    if new_state:
                        res = cols[2].radio(f"Res_{ab}", ["S", "I", "R", "ND"], key=f"res_{ab}", horizontal=True, label_visibility="collapsed")
                        cols[3].text_input(f"CMI_{ab}", key=f"cmi_{ab}", label_visibility="collapsed", placeholder="CMI", disabled=(res not in ["S", "I", "R"]))
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. GUARDADO Y NAVEGACIÓN ---
    def guardar():
        st.session_state.datos_completos["Polimicrobiana"] = {"Es_Polimicrobiana": st.session_state.es_poli}

    st.divider()
    col_atras, col_guardar = st.columns([1, 4])
    if col_atras.button("⬅️ Atrás"):
        guardar()
        idx = ORDEN.index(st.session_state.pagina_actual)
        st.session_state.pagina_actual = ORDEN[idx - 1]
        st.rerun()
    if col_guardar.button("Guardar registro y continuar"):
        guardar()
        idx = ORDEN.index(st.session_state.pagina_actual)
        if idx < len(ORDEN) - 1:
            st.session_state.pagina_actual = ORDEN[idx + 1]
            st.rerun()

if __name__ == "__main__":
    render()
