import streamlit as st
from config import ORDEN

def render():
    st.set_page_config(layout="wide")
    st.title("Diagnóstico Microbiológico")

    # --- 0. RECUPERACIÓN DE ESTADOS ---
    hab_micro = st.session_state.get("habilitar_microbiologia", False)
    hab_hemo = st.session_state.get("habilitar_hemocultivos", False)
    m = st.session_state.datos_completos.get("Micro", {})

    if not hab_micro:
        st.warning("⚠️ Los campos de microbiología están inhabilitados porque la detección fue 'Definida clínicamente'.")

    # --- CSS ---
    st.markdown("""<style>.highlight-row { background-color: #e6f3ff; padding: 5px 10px; border-radius: 8px; margin-bottom: 2px; border: 1px solid #d1e7fd; }</style>""", unsafe_allow_html=True)

    # --- 1. HEMOCULTIVOS (ITS) ---
    st.markdown("### Hemocultivos")
    hemocultivo_its = st.radio("¿Se tomaron hemocultivos para ITS?", ["No", "Sí"], key="k_hemo_its", index=["No", "Sí"].index(m.get("Hemo_ITS", "No")), horizontal=True, disabled=not (hab_micro and hab_hemo))
    
    if hemocultivo_its == "Sí":
        c_hem1, c_hem2, c_hem3 = st.columns(3)
        c_hem1.radio("SANGRE PERIFÉRICA", ["No", "Sí"], index=None, horizontal=True)
        c_hem2.radio("SANGRE POR CATETÉR CENTRAL", ["No", "Sí"], index=None, horizontal=True)
        c_hem3.radio("PUNTA DE CATETÉR CENTRAL", ["No", "Sí"], index=None, horizontal=True)

    # --- 2. PREGUNTA GENERAL ---
    se_tomo_muestra = st.radio("¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", ["No", "Sí"], key="k_tomo_muestra", index=["No", "Sí"].index(m.get("Tomada", "No")), horizontal=True, disabled=not hab_micro)

    if (se_tomo_muestra == "Sí" or hemocultivo_its == "Sí") and hab_micro:
        c1, c2 = st.columns(2)
        with c1:
            st.date_input("FECHA DE TOMA", format="DD/MM/YYYY")
            st.selectbox("LABORATORIO", ["De la unidad", "InDRE", "LESP", "LAVE", "PRIVADO/SUBROGADO", "OTRO"], index=None, placeholder="Seleccione...")
        with c2:
            st.date_input("FECHA DE RESULTADO", format="DD/MM/YYYY")
            st.selectbox("TIPO DE MUESTRA", ["Orina de chorro medio", "Aspirado bronquial", "Sangre periferica", "Liquido cefaloraquideo", "Otro"], index=None, placeholder="Seleccione...")

        tecnicas = ["Bioquímicas manuales", "Inmunocromatografía", "Manuales API", "VITEK (automatizada)", "MicroScan (automatizada)", "Espectrometría de masas. MALDI-TOF", "PCR (moleculares)"]
        st.selectbox("TÉCNICA PARA DIAGNÓSTICO MICROBIOLÓGICO", tecnicas, index=None, placeholder="Seleccione...")
        
        resultado = st.radio("RESULTADO", ["CON DESARROLLO/ POSITIVO", "SIN DESARROLLO/ NEGATIVO", "RECHAZADA"], index=None)

        if resultado == "CON DESARROLLO/ POSITIVO":
            microorganismos = sorted(["Absidia spp", "Acinetobacter baumannii", "Aspergillus spp.", "Bacteroides fragilis group", "Burkholderia cepacia complex", "Candida albicans", "Candida auris", "Citrobacter freundii", "Clostridioides difficile", "Enterobacter cloacae complex", "Enterococcus faecalis", "Enterococcus faecium", "Escherichia coli", "Klebsiella aerogenes", "Klebsiella oxytoca", "Klebsiella pneumoniae", "Mycobacterium abscessus", "Proteus mirabilis", "Providencia stuartii", "Pseudomonas aeruginosa", "Serratia marcescens", "Staphylococcus aureus", "Staphylococcus coagulasa negativo", "Staphylococcus epidermidis", "Stenotrophomonas maltophilia", "Streptococcus agalactiae", "Streptococcus pneumoniae", "Streptococcus spp."])
            micro = st.selectbox("MICROORGANISMO AISLADO", microorganismos, index=None, placeholder="Seleccione...")

        # --- PRUEBA DE SUSCEPTIBILIDAD ---
        st.subheader("Prueba de Susceptibilidad")
        st.caption("Selecciona la opción según corresponda: S=Susceptible, I=Intermedio, R=Resistente, ND=No determinada. *CMI= Concentración mínima inhibitoria.")
        
        realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD ANTIMICROBIANA?", ["No", "Sí"], horizontal=True)
        
        if realizo_susp == "Sí":
            st.selectbox("TÉCNICA PARA SUSCEPTIBILIDAD", ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"], index=None, placeholder="Seleccione...")
            
            # Encabezados
            col_head1, col_head2, col_head3 = st.columns([2, 2, 1])
            col_head1.write("**ANTIMICROBIANO**")
            col_head2.write("**RESULTADO (S/I/R/ND)**")
            col_head3.write("**CMI**")
            
            antibioticos = [
                "AMIKACINA", "AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", 
                "AZTREONAM", "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", 
                "CEFOXITINA", "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", 
                "CEFTOLOZANE-TAZOBACTAM", "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", 
                "DAPTOMICINA", "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA", 
                "IMIPENEM", "ITRACONAZOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "MICAFUNGINA", 
                "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM", "POSACONAZOL", 
                "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA", "TRIMETOPRIM-SULFAMETOXAZOL", 
                "VANCOMICINA", "VORICONAZOL"
            ]
            
            for ab in antibioticos:
                key_check = f"check_{ab}"
                with st.container():
                    st.markdown(f'<div class="{"highlight-row" if st.session_state.get(key_check) else ""}">', unsafe_allow_html=True)
                    c1, c2, c3 = st.columns([2, 2, 1])
                    if c1.checkbox(f"**{ab}**", key=key_check):
                        res = c2.radio(f"Res_{ab}", ["S", "I", "R", "ND"], key=f"res_{ab}", horizontal=True, label_visibility="collapsed")
                        if res in ["S", "I", "R"]:
                            c3.text_input(f"CMI_{ab}", key=f"cmi_{ab}", label_visibility="collapsed", placeholder="CMI")
                        else:
                            c3.text_input(f"CMI_{ab}", key=f"cmi_{ab}", label_visibility="collapsed", placeholder="N/A", disabled=True)
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- GUARDADO ---
    def guardar():
        st.session_state.datos_completos["Micro"] = {"Hemo_ITS": st.session_state.get("k_hemo_its", "No"), "Tomada": st.session_state.get("k_tomo_muestra", "No")}

    st.divider()
    if st.button("⬅️ Atrás"):
        guardar()
        idx = ORDEN.index(st.session_state.pagina_actual)
        st.session_state.pagina_actual = ORDEN[idx - 1]
        st.rerun()
    if st.button("Guardar registro y continuar"):
        guardar()
        st.session_state.pagina_actual = "Tratamiento de IAAS" if not hab_micro else ORDEN[ORDEN.index(st.session_state.pagina_actual) + 1]
        st.rerun()

if __name__ == "__main__":
    render()
        
