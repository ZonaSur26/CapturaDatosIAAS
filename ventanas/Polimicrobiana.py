import streamlit as st
from config import ORDEN

def render():
    st.set_page_config(layout="wide")
    st.title("Infección Polimicrobiana")

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
        # Lista completa de microorganismos
        microorganismos = sorted(["Absidia spp", "Achromobacter denitrificans", "Acinetobacter baumannii", "Aspergillus flavus", "Bacteroides fragilis group", "Burkholderia cepacia", "Candida albicans", "Candida auris", "Citrobacter freundii", "Clostridioides difficile", "Enterobacter cloacae", "Enterococcus faecalis", "Escherichia coli", "Klebsiella pneumoniae", "Mycobacterium abscessus", "Proteus mirabilis", "Providencia stuartii", "Pseudomonas aeruginosa", "Serratia marcescens", "Staphylococcus aureus", "Staphylococcus epidermidis", "Stenotrophomonas maltophilia", "Streptococcus agalactiae", "Streptococcus pneumoniae", "Streptococcus spp.", "Virus de Inmunodeficiencia Humana", "Virus sincitial respiratorio"])
        
        micro = st.selectbox("MICROORGANISMO AISLADO", microorganismos, index=None, placeholder="Seleccione...")

        # --- 3. SUSCEPTIBILIDAD (Con diseño de Microbiología) ---
        st.subheader("Prueba de Susceptibilidad")
        st.caption("Selecciona la opción según corresponda: S=Susceptible. I= Intermedio. R= Resistente. ND= No determinada. *CMI= Se refiere a la concentración mínima inhibitoria.")
        
        realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD ANTIMICROBIANA?", ["No", "Sí"], horizontal=True)
        
        if realizo_susp == "Sí":
            st.selectbox("TÉCNICA PARA SUSCEPTIBILIDAD", ["CMI", "EPSILOMETRIA", "ELUSIÓN DE DISCO", "DISCO DIFUSIÓN"], index=None, placeholder="Seleccione...")
            
            antibioticos = ["AMIKACINA", "AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", "AZTREONAM", "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA", "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANE-TAZOBACTAM", "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", "DAPTOMICINA", "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA", "IMIPENEM", "ITRACONZAOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "MICAFUNGINA", "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM", "POSACONAZOL", "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA", "TRIMETOPRIM-SULFAMETOXAZOL", "VANCOMICINA", "VORICONAZOL"]
            
            c1, c2, c3, c4 = st.columns([0.5, 2, 2, 1])
            c1.write("**Sel**"); c2.write("**ANTIMICROBIANO**"); c3.write("**S / I / R / ND**"); c4.write("**CMI**")
            
            for ab in antibioticos:
                key_check = f"check_{ab}"
                with st.container():
                    st.markdown(f'<div class="{"highlight-row" if st.session_state.get(key_check) else ""}">', unsafe_allow_html=True)
                    cols = st.columns([0.5, 2, 2, 1])
                    if cols[0].checkbox("", key=key_check):
                        cols[1].markdown(f"**{ab}**")
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
