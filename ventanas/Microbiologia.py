import streamlit as st
from config import ORDEN

def render():
    st.set_page_config(layout="wide")
    st.title("Diagnóstico Microbiológico")

    # --- 0. RECUPERACIÓN DE ESTADOS ---
    iaas_data = st.session_state.datos_completos.get("IAAS", {})
    m = st.session_state.datos_completos.get("Micro", {})
    hab_micro = (iaas_data.get("tipo_deteccion") == "Confirmada por laboratorio")
    hab_hemo = st.session_state.get("habilitar_hemocultivos", False)

    if not hab_micro:
        st.warning("⚠️ Los campos de microbiología están inhabilitados porque la detección fue 'Definida clínicamente'.")

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
    hemocultivo_its = st.radio("¿Se tomaron hemocultivos para ITS?", ["No", "Sí"], key="k_hemo_its", index=["No", "Sí"].index(m.get("Hemo_ITS", "No")), horizontal=True, disabled=not (hab_micro and hab_hemo))
    
    if hemocultivo_its == "Sí":
        c_hem1, c_hem2, c_hem3 = st.columns(3)
        c_hem1.radio("SANGRE PERIFÉRICA", ["No", "Sí"], key="sp", index=["No", "Sí"].index(m.get("sp", "No")), horizontal=True)
        c_hem2.radio("SANGRE POR CATETÉR CENTRAL", ["No", "Sí"], key="scc", index=["No", "Sí"].index(m.get("scc", "No")), horizontal=True)
        c_hem3.radio("PUNTA DE CATETÉR CENTRAL", ["No", "Sí"], key="pcc", index=["No", "Sí"].index(m.get("pcc", "No")), horizontal=True)

    # --- 2. PREGUNTA GENERAL ---
    se_tomo_muestra = st.radio("¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", ["No", "Sí"], key="k_tomo_muestra", index=["No", "Sí"].index(m.get("Tomada", "No")), horizontal=True, disabled=not hab_micro)

    if (se_tomo_muestra == "Sí" or hemocultivo_its == "Sí") and hab_micro:
        c1, c2 = st.columns(2)
        with c1:
            st.date_input("FECHA DE TOMA", key="k_f_toma", value=m.get("Fecha_Toma") or None, format="DD/MM/YYYY")
            lab_opciones = ["De la unidad", "InDRE", "LESP", "LAVE", "PRIVADO/SUBROGADO", "OTRO"]
            st.selectbox("LABORATORIO", lab_opciones, key="k_lab", index=lab_opciones.index(m.get("Lab")) if m.get("Lab") in lab_opciones else None, placeholder="Seleccione...")
        with c2:
            st.date_input("FECHA DE RESULTADO", key="k_f_res", value=m.get("Fecha_Res") or None, format="DD/MM/YYYY")
            muestras_opciones = ["Orina de chorro medio", "Aspirado bronquial", "Sangre periferica", "Liquido cefaloraquideo", "Otro"]
            st.selectbox("TIPO DE MUESTRA", muestras_opciones, key="k_muestra", index=muestras_opciones.index(m.get("Muestra")) if m.get("Muestra") in muestras_opciones else None, placeholder="Seleccione...")

        tecnicas = ["Bioquímicas manuales", "Inmunocromatografía", "Manuales API", "VITEK (automatizada)", "MicroScan (automatizada)", "Espectrometría de masas. MALDI-TOF", "PCR (moleculares)"]
        st.selectbox("TÉCNICA PARA DIAGNÓSTICO MICROBIOLÓGICO", tecnicas, key="k_tecnica", index=tecnicas.index(m.get("Tecnica")) if m.get("Tecnica") in tecnicas else None, placeholder="Seleccione...")
        
        resultado = st.radio("RESULTADO", ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"], key="k_res", index=["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"].index(m.get("Resultado")) if m.get("Resultado") in ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"] else None)

        if resultado == "CON DESARROLLO/ POSITIVO":
            microorganismos = sorted(["Absidia spp", "Acinetobacter baumannii", "Aspergillus spp.", "Bacteroides fragilis group", "Burkholderia cepacia complex", "Candida albicans", "Candida auris", "Citrobacter freundii", "Clostridioides difficile", "Enterobacter cloacae complex", "Enterococcus faecalis", "Enterococcus faecium", "Escherichia coli", "Klebsiella aerogenes", "Klebsiella oxytoca", "Klebsiella pneumoniae", "Mycobacterium abscessus", "Proteus mirabilis", "Providencia stuartii", "Pseudomonas aeruginosa", "Serratia marcescens", "Staphylococcus aureus", "Staphylococcus coagulasa negativo", "Staphylococcus epidermidis", "Stenotrophomonas maltophilia", "Streptococcus agalactiae", "Streptococcus pneumoniae", "Streptococcus spp.", "Virus de Inmunodeficiencia Humana", "Virus sincitial respiratorio"])
            st.selectbox("MICROORGANISMO AISLADO", microorganismos, key="k_micro", index=microorganismos.index(m.get("MicroOrg")) if m.get("MicroOrg") in microorganismos else None, placeholder="Seleccione...")

            # --- SUSCEPTIBILIDAD ---
            st.subheader("Prueba de Susceptibilidad")
            st.caption("Selecciona la opción según corresponda: S=Susceptible. I= Intermedio. R= Resistente. ND= No determinada. *CMI= Se refiere a la concentración mínima inhibitoria.")
            realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD?", ["No", "Sí"], key="k_susp", index=["No", "Sí"].index(m.get("Susp", "No")), horizontal=True)
            
            if realizo_susp == "Sí":
                antibioticos = ["AMIKACINA", "AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", "AZTREONAM", "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA", "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANE-TAZOBACTAM", "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", "DAPTOMICINA", "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA", "IMIPENEM", "ITRACONAZOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "MICAFUNGINA", "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM", "POSACONAZOL", "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA", "TRIMETOPRIM-SULFAMETOXAZOL", "VANCOMICINA", "VORICONAZOL"]
                
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
                            cols[3].text_input(f"CMI_{ab}", key=f"cmi_{ab}", value=m.get(f"cmi_{ab}", ""), label_visibility="collapsed", placeholder="CMI", disabled=(res not in ["S", "I", "R"]))
                        st.markdown('</div>', unsafe_allow_html=True)

    # --- GUARDADO SEGURO ---
    def guardar():
        data = {
            "Hemo_ITS": st.session_state.get("k_hemo_its", "No"),
            "sp": st.session_state.get("sp", "No"),
            "scc": st.session_state.get("scc", "No"),
            "pcc": st.session_state.get("pcc", "No"),
            "Tomada": st.session_state.get("k_tomo_muestra", "No"),
            "Susp": st.session_state.get("k_susp", "No"),
            "MicroOrg": st.session_state.get("k_micro"),
            "Resultado": st.session_state.get("k_res")
        }
        antibioticos = ["AMIKACINA", "AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", "AZTREONAM", "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA", "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANE-TAZOBACTAM", "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", "DAPTOMICINA", "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA", "IMIPENEM", "ITRACONAZOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "MICAFUNGINA", "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM", "POSACONAZOL", "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA", "TRIMETOPRIM-SULFAMETOXAZOL", "VANCOMICINA", "VORICONAZOL"]
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
