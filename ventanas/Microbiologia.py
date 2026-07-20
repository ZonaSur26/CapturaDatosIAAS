import streamlit as st
from config import ORDEN  # Importamos ORDEN desde tu archivo de configuración

def render():
    st.set_page_config(layout="wide")
    st.title("Diagnóstico Microbiológico")

    # --- 0. RECUPERACIÓN DE DATOS GUARDADOS ---
    # Recuperamos el estado de IAAS para condiciones y datos previos de Micro
    iaas_data = st.session_state.datos_completos.get("IAAS", {})
    m = st.session_state.datos_completos.get("Micro", {})

    hab_micro = (iaas_data.get("tipo_deteccion") == "Confirmada por laboratorio")
    
    if not hab_micro:
        st.warning("⚠️ Los campos de microbiología están inhabilitados porque la detección fue 'Definida clínicamente'.")

    # --- CSS ---
    st.markdown("""<style>.highlight-row { background-color: #e6f3ff; padding: 5px 10px; border-radius: 8px; margin-bottom: 2px; border: 1px solid #d1e7fd; }</style>""", unsafe_allow_html=True)

    # --- 1. HEMOCULTIVOS (ITS) ---
    st.markdown("### Hemocultivos")
    # Persistencia con g.get para el índice
    hemocultivo_its = st.radio(
        "¿Se tomaron hemocultivos para ITS?", ["No", "Sí"], 
        key="k_hemo_its",
        index=["No", "Sí"].index(m.get("Hemo_ITS", "No")), 
        horizontal=True,
        disabled=not hab_micro
    )
    
    if hemocultivo_its == "Sí":
        c_hem1, c_hem2, c_hem3 = st.columns(3)
        c_hem1.radio("SANGRE PERIFÉRICA", ["No", "Sí"], key="sp", index=0, horizontal=True)
        c_hem2.radio("SANGRE POR CATETÉR CENTRAL", ["No", "Sí"], key="scc", index=0, horizontal=True)
        c_hem3.radio("PUNTA DE CATETÉR CENTRAL", ["No", "Sí"], key="pcc", index=0, horizontal=True)

    # --- 2. PREGUNTA GENERAL ---
    se_tomo_muestra = st.radio(
        "¿SE TOMÓ MUESTRA PARA DIAGNÓSTICO MICROBIOLÓGICO?", ["No", "Sí"], 
        key="k_tomo_muestra",
        index=["No", "Sí"].index(m.get("Tomada", "No")),
        horizontal=True,
        disabled=not hab_micro
    )

    if (se_tomo_muestra == "Sí" or hemocultivo_its == "Sí") and hab_micro:
        c1, c2 = st.columns(2)
        with c1:
            fecha_toma = st.date_input("FECHA DE TOMA", value=m.get("Fecha_Toma") or None, format="DD/MM/YYYY")
            lab_opciones = ["De la unidad", "InDRE", "LESP", "LAVE", "PRIVADO/SUBROGADO", "OTRO"]
            laboratorio = st.selectbox("LABORATORIO", lab_opciones, index=lab_opciones.index(m.get("Lab")) if m.get("Lab") in lab_opciones else None, placeholder="Seleccione...")
            if laboratorio == "OTRO":
                st.text_input("Especifique otro laboratorio:", key="otro_lab", value=m.get("Otro_Lab", ""))
        with c2:
            fecha_resultado = st.date_input("FECHA DE RESULTADO", value=m.get("Fecha_Res") or None, format="DD/MM/YYYY")
            muestras_opciones = ["Orina de chorro medio", "Orina por puncion suprapubica", "Orina cateter vesical", "Sonda de entrada por salida", "Aspirado bronquial", "Aspirado traqueal", "Esputo inducido", "Esputo espontaneo", "Lavado bronco alveolar", "Biopsia transbronquial", "Biopsia pulmonar", "Biopsia pleural", "Sangre periferica", "Aspirado", "Biopsia", "Exudado faringeo", "Drenaje otico", "Sangre por cateter central", "Punta de cateter central", "Drenaje", "Liquido pericardico", "Heces", "Aspirado de absceso o secrecion de herida", "Hisopado de herida quirurgica +score Q", "Liquidos organicos", "Biopsia cuantitativa", "Aspirado de absceso", "Hisopado + score Q", "Liquido sinovial", "Sonicado de piezas protesicas para cultivo", "Hisopado conjuntival", "Raspado ocular", "Aspirado de humor vitreo", "Aspirado de humor acuoso", "Lavado ocular", "Liquido cefaloraquideo", "Liquido peritoneal", "Otro"]
            tipo_muestra = st.selectbox("TIPO DE MUESTRA", muestras_opciones, index=muestras_opciones.index(m.get("Muestra")) if m.get("Muestra") in muestras_opciones else None, placeholder="Seleccione...")

        # ... (Mantén aquí tu lógica de técnicas, resultados y susceptibilidad con sus respectivos keys y value=g.get()) ...

    # --- FUNCIÓN DE GUARDADO ---
    def guardar():
        st.session_state.datos_completos["Micro"] = {
            "Hemo_ITS": st.session_state.get("k_hemo_its", "No"),
            "Tomada": st.session_state.get("k_tomo_muestra", "No"),
            "Fecha_Toma": st.session_state.get("FECHA DE TOMA"),
            "Lab": st.session_state.get("LABORATORIO"),
            "Muestra": st.session_state.get("TIPO DE MUESTRA")
        }

    # --- NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])
    
    with col_atras:
        if st.button("⬅️ Atrás"):
            guardar()
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx > 0:
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()

    with col_guardar:
        if st.button("Guardar registro y continuar"):
            guardar()
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[idx + 1]
                st.rerun()

if __name__ == "__main__":
    render()
