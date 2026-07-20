import streamlit as st
from config import ORDEN

def render():
    st.set_page_config(layout="wide")
    st.title("Diagnóstico Microbiológico")

    # --- 0. RECUPERACIÓN DE ESTADOS ---
    iaas_data = st.session_state.datos_completos.get("IAAS", {})
    m = st.session_state.datos_completos.get("Micro", {})
    hab_micro = (iaas_data.get("Deteccion") == "Confirmada por laboratorio")
    hab_hemo = st.session_state.get("habilitar_hemocultivos", False)

    if not hab_micro:
        st.warning("⚠️ Los campos de microbiología están inhabilitados porque la detección fue 'Definida clínicamente'.")

    # Lista completa de antibióticos
    antibioticos = [
        "AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA", "AZTREONAM", 
        "CASPOFUNGINA", "CEFAZOLINA", "CEFEPIME", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA", 
        "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANE-TAZOBACTAM", 
        "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", "DAPTOMICINA", 
        "ERITROMICINA", "ERTAPENEM", "FLUCONAZOL", "FOSFOMICINA", "GENTAMICINA", 
        "IMIPENEM", "ITRACONAZOL", "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", 
        "MICAFUNGINA", "NITROFURANTOINA", "OXACILINA", "PENICILINA", "PIPERACILINA-TAZOBACTAM", 
        "POSACONAZOL", "RIFAMPICINA", "TETRACICLINA", "TIGECICLINA", "TRIMETOPRIM-SULFAMETOXAZOL", 
        "VANCOMICINA", "VORICONAZOL"
    ]

    # --- 1. HEMOCULTIVOS Y MUESTRAS ---
    hemocultivo_its = st.radio("¿Se tomaron hemocultivos para ITS?", ["No", "Sí"], key="k_hemo_its", index=["No", "Sí"].index(m.get("Hemo_ITS", "No")), horizontal=True, disabled=not (hab_micro and hab_hemo))
    
    se_tomo_muestra = st.radio("¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", ["No", "Sí"], key="k_tomo_muestra", index=["No", "Sí"].index(m.get("Tomada", "No")), horizontal=True, disabled=not hab_micro)

    if (se_tomo_muestra == "Sí" or hemocultivo_its == "Sí") and hab_micro:
        # (Aquí va tu código de laboratorio, fechas, tipo de muestra, técnicas, resultado y microorganismo...)
        # ... (Mantén tu lógica existente aquí) ...

        # --- PRUEBA DE SUSCEPTIBILIDAD ---
        st.subheader("Prueba de Susceptibilidad")
        realizo_susp = st.radio("¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD?", ["No", "Sí"], key="k_susp", index=["No", "Sí"].index(m.get("Susp", "No")), horizontal=True)
        
        if realizo_susp == "Sí":
            h1, h2, h3 = st.columns([2, 2, 1])
            h1.write("**ANTIMICROBIANO**"); h2.write("**RESULTADO**"); h3.write("**CMI**")
            
            for ab in antibioticos:
                check_key = f"check_{ab}"
                with st.container():
                    c1, c2, c3 = st.columns([2, 2, 1])
                    if c1.checkbox(f"**{ab}**", key=check_key, value=m.get(check_key, False)):
                        c2.radio(f"Res_{ab}", ["S", "I", "R", "ND"], key=f"res_{ab}", index=["S", "I", "R", "ND"].index(m.get(f"res_{ab}", "ND")), horizontal=True, label_visibility="collapsed")
                        c3.text_input(f"CMI_{ab}", key=f"cmi_{ab}", value=m.get(f"cmi_{ab}", ""), label_visibility="collapsed", placeholder="CMI")

    # --- GUARDADO CENTRALIZADO ---
    def guardar():
        data = {
            "Hemo_ITS": st.session_state.get("k_hemo_its", "No"),
            "Tomada": st.session_state.get("k_tomo_muestra", "No"),
            "Susp": st.session_state.get("k_susp", "No")
        }
        # Guardado dinámico de la tabla completa
        for ab in antibioticos:
            data[f"check_{ab}"] = st.session_state.get(f"check_{ab}", False)
            data[f"res_{ab}"] = st.session_state.get(f"res_{ab}", "ND")
            data[f"cmi_{ab}"] = st.session_state.get(f"cmi_{ab}", "")
        st.session_state.datos_completos["Micro"] = data

    # --- NAVEGACIÓN ---
    st.divider()
    c_atras, c_adelante = st.columns([1, 4])
    if c_atras.button("⬅️ Atrás"): guardar(); st.session_state.pagina_actual = ORDEN[ORDEN.index(st.session_state.pagina_actual) - 1]; st.rerun()
    if c_adelante.button("Guardar y continuar"): guardar(); st.session_state.pagina_actual = ORDEN[ORDEN.index(st.session_state.pagina_actual) + 1]; st.rerun()

if __name__ == "__main__":
    render()
