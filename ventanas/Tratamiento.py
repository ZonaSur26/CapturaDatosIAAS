import streamlit as st
from config import ORDEN

def render():
    st.set_page_config(layout="wide")
    st.title("Tratamiento de IAAS")
    
    # --- 1. PERSISTENCIA: Recuperación de datos guardados ---
    if "Tratamiento" not in st.session_state.datos_completos:
        st.session_state.datos_completos["Tratamiento"] = {}
    data = st.session_state.datos_completos["Tratamiento"]
    
    st.subheader("Esquema Antimicrobiano")
    
    lista_ab = sorted([
        "ABACAVIR", "ABACAVIR/ LAMIVUDINA", "ACICLOVIR", "ACIDO UNDECILENICO / UNDECILENATO DE ZINC",
        "ACIDO UNDECILENICO / UNDECILENATO DE ZINC / TRICLOSAN", "ALBENDAZOL", "ALBENDAZOL/QUINFAMIDA",
        "AMFOTERICINA B", "AMIKACINA", "AMOXICILINA", "AMOXICILINA/ PIVOXIL SULBACTAM",
        "AMOXICILINA/ SULBACTAM", "AMOXICILINA/ACIDO CLAVULANICO", "AMPICILINA", "AMPICILINA/ DICLOXACILINA",
        "AMPICILINA/SULBACTAM", "ANFOTERICINA B ANIDULAFUNGINA", "AZITROMICINA", "AZTREONAM",
        "BENCILPENICILINA", "BENCILPENICILINA PROCAINICA/ BENCILPENICILINA SODICA",
        "BENCILPENICILINA/ CLEMIZOL BENCILPENICILINA", "BENCINAMIDA", "BIFONAZOL BUTENAFINA",
        "CAOLIN/ NEOMICINA/ PECTINA", "CASPOFUNGINA", "CEFADROXILO", "CEFALEXINA", "CEFAZOLINA",
        "CEFDINIR", "CEFEPIMA", "CEFIXIMA", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA", "CEFPODOXIMA",
        "CEFTAZIDIMA", "CEFTAZIDIMA/AVIBACTAM", "CEFTIBUTENO", "CEFTOLOZANO/TAZOBACTAM", "CEFTRIAXONA",
        "CEFUROXIMA", "CETIRIZINA", "CICLOPIROXOLAMINA", "CILOSTAZOL", "CIPROFLOXACINO", "CLARITROMICINA",
        "CLINDAMICINA", "CLORANFENICOL", "CLOSTRIDIOPEPTIDASA/CLORANFENICOL", "CLOTRIMAZOL",
        "CLOTRIMAZOL/DEXAMETASONA/NEOMICINA", "COLISTIMETATO", "COLISTINA", "DAPTOMICINA", "DICLOXACILINA",
        "DIDANOSINA", "DIYODOHIDROXIQUINOLEINA", "DIYODOHIDROXIQUINOLEINA/FTALILSULFATIAZOL/PAPAVERINA",
        "DIYODOHIDROXIQUINOLEINA/METRONIDAZOL", "DOXICICLINA", "EMTRICITABINA",
        "EMTRICITABINA/TENOFOVIR DISOPROXILO", "ENFUVIRTIDA", "ENOXOLONA", "ENTECAVIR", "ERITROMICINA",
        "ERTAPENEM", "ESPIRAMICINA", "ESTREPTOMICINA", "EVEROLIMUS", "FENTICONAZOL", "FLUCONAZOL",
        "FLUCONAZOL/TINIDAZOL", "FLUTRIMAZOL", "FOSFOMICINA", "FUSIDATO", "GATIFLOXACINO",
        "GEMIFLOXACINO", "GENTAMICINA", "HEMEZOL", "IMIPENEM", "IMIPENEM/CILASTATINA", "INOSINA",
        "ISOCONAZOL", "ISONIAZIDA", "ISONIAZIDA/PIRAZINAMIDA/RIFAMPICINA", "ITRACONAZOL",
        "ITRACONAZOL/SECNIDAZOL", "IVERMECTINA", "KETOCONAZOL", "KETOCONAZOL/TINIDAZOL/CLINDAMICINA",
        "LAMIVUDINA", "LAMIVUDINA/ZIDOVUDINA", "LEVOFLOXACINO", "LIDOCAINA/NEOMICINA/POLIMIXINA B",
        "LIMECICLINA", "LINCOMICINA", "LINEZOLID", "LOPINAVIR/RITONAVIR", "LOTEPRENDOL/TOBRAMICINA",
        "MARAVIROC", "MEBENDAZOL", "MEBENDAZOL/QUINFAMIDA", "MEBENDAZOL/TINIDAZOL", "MEROPENEM",
        "METISOPRINOL", "METRONIDAZOL", "METRONIDAZOL/NISTATINA", "METRONIDAZOL/NISTATINA/FLUOCINOLONA",
        "METRONIDAZOL/NITRATO DE MICONAZOL", "METRONIDAZOL/YODIHROXIQUINOLEINA",
        "METRONIDAZOL/YODOHIDROXIQUINOLEINA", "MICAFUNGINA", "MICONAZOL", "MICONAZOL/OXIDO DE ZINC",
        "MINOCICLINA", "MOXIFLOXACINO", "MOXIFLOXACINO/DEXAMETASONA", "MUPIROCINA", "NADIFLOXACINO",
        "NEOMICINA/POLIMIXINA B/FENILEFRINA/FLUOCINOLONA", "NEOMICINA/POLIMIXINA B/FLUOCINOLONA",
        "NEOMICINA/POLIMIXINA B/LIDOCAINA/FLUOCINOLONA", "NEVIRAPINA", "NIFURATEL/NISTATINA",
        "NIFUROXAZIDA/METRONIDAZOL", "NISTATINA", "NITAZOXANIDA", "NORFLOXACINO", "OFLOXACINO",
        "OSELTAMIVIR", "OXACILINA", "OXITETRACICILINA", "OXITETRACICILINA/POLIMIXINA B", "PENICILINA",
        "PERMETRINA", "PIPERACILINA/TAZOBACTAM", "PIRANTEL", "PIRIMETAMINA", "POLICRESULENO",
        "POSACONAZOL", "RALTEGRAVIR", "RIBAVIRINA", "RIFAMICINA SV", "RIFAMPICINA",
        "RIFAMPICINA/ISONIAZIDA/PIRAZINAMIDA/ETAMBUTOL", "RIFAXIMINA", "RIMANTADINA", "SECNIDAZOL",
        "SULFACETAMIDA", "SULFAMETOXAZOL/TRIMETOPRIMA", "TEDIZOLID", "TERBINAFINA", "TETRACICLINA",
        "TETRACICLINA/CLORANFENICOL/LIDOCAINA/BETA-HIDROXIPROPILTEOFILINA/GUAIFENESINA",
        "TIGECIGLINA", "TINIDAZOL", "TOBRAMICINA", "TRIMETROPIN/SULFAMETOXAZOL", "VALACICLOVIR",
        "VALGANCICLOVIR", "VANCOMICINA", "VORICONAZOL", "ZANAMIVIR", "ZIDOVUDINA"
    ])

    # Cabeceras
    c_ab, c_ini, c_fin = st.columns([2, 1, 1])
    c_ab.markdown("**ANTIMICROBIANO**")
    c_ini.markdown("**FECHA DE INICIO**")
    c_fin.markdown("**FECHA DE TÉRMINO**")

    # 5 Filas de captura
    for i in range(5):
        # Recuperar valores previos guardados
        fila = data.get(f"Fila_{i}", {})
        
        c_ab, c_ini, c_fin = st.columns([2, 1, 1])
        with c_ab:
            st.selectbox(f"AB_{i}", lista_ab, index=lista_ab.index(fila["AB"]) if fila.get("AB") in lista_ab else None, label_visibility="collapsed", key=f"ab_{i}", placeholder="Seleccione...")
        with c_ini:
            st.date_input(f"INI_{i}", value=fila.get("Inicio") if fila.get("Inicio") else None, label_visibility="collapsed", key=f"ini_{i}", format="DD/MM/YYYY")
        with c_fin:
            st.date_input(f"FIN_{i}", value=fila.get("Fin") if fila.get("Fin") else None, label_visibility="collapsed", key=f"fin_{i}", format="DD/MM/YYYY")

    # --- LÓGICA DE GUARDADO ---
    def guardar():
        nuevo_tratamiento = {}
        for i in range(5):
            ab = st.session_state.get(f"ab_{i}")
            if ab:
                nuevo_tratamiento[f"Fila_{i}"] = {
                    "AB": ab, 
                    "Inicio": st.session_state.get(f"ini_{i}"), 
                    "Fin": st.session_state.get(f"fin_{i}")
                }
        st.session_state.datos_completos["Tratamiento"] = nuevo_tratamiento

    # --- NAVEGACIÓN ---
    st.divider()
    c_atras, c_guardar = st.columns([1, 4])
    
    with c_atras:
        if st.button("⬅️ Atrás"):
            guardar()
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx > 0:
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()

    with c_guardar:
        if st.button("Guardar registro y continuar"):
            guardar()
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[idx + 1]
                st.rerun()

if __name__ == "__main__":
    render()
