import streamlit as st
import sys
from config import ORDEN

# Función para forzar mayúsculas en tiempo real
def to_upper(key):
    st.session_state[key] = str(st.session_state[key]).upper()

def render():
    st.title("Antecedentes Personales Patológicos")
    st.subheader("Seleccione los antecedentes presentes")

    antecedentes_lista = [
        "PREMATUREZ", "BAJO PESO AL NACER", "DIABETES MELLITUS", 
        "HIPERTENSIÓN ARTERIAL SISTÉMICA", "SOBREPESO", "OBESIDAD", "TABAQUISMO",
        "DESNUTRICIÓN", "ENFERMEDAD RENAL CRÓNICA", "EPOC", 
        "VIH/SIDA", "INMUNOSUPRESIÓN", "CANCER"
    ]

    # Recuperar datos previos para marcar los checkboxes
    g = st.session_state.datos_completos.get("Antecedentes", {})

    # Layout en 2 columnas
    col1, col2 = st.columns(2)
    mitad = (len(antecedentes_lista) + 1) // 2
    
    # Marcamos los checkboxes según los datos guardados
    def is_checked(item):
        return g.get(item, "NO") == "SÍ"

    antecedentes_seleccionados = {}
    
    with col1:
        for item in antecedentes_lista[:mitad]:
            antecedentes_seleccionados[item] = st.checkbox(item, key=f"check_{item}", value=is_checked(item))
    with col2:
        for item in antecedentes_lista[mitad:]:
            antecedentes_seleccionados[item] = st.checkbox(item, key=f"check_{item}", value=is_checked(item))

    # --- CAMPO "OTRO" ---
    st.markdown("---")
    es_otro_inicial = g.get("OTRO", "NO APLICA") != "NO APLICA"
    es_otro = st.checkbox("OTRO", key="check_otro", value=es_otro_inicial)
    
    if es_otro:
        st.text_input(
            "Especifique el otro antecedente:", 
            key="otro_text", 
            value=g.get("OTRO") if es_otro_inicial else "",
            on_change=to_upper, 
            args=["otro_text"]
        )

    # --- LÓGICA DE GUARDADO ---
    def guardar_antecedentes():
        datos_formateados = {k: ("SÍ" if v is True else "NO") for k, v in antecedentes_seleccionados.items()}
        datos_formateados["OTRO"] = st.session_state.get("otro_text", "").upper() if st.session_state.check_otro else "NO APLICA"
        st.session_state.datos_completos["Antecedentes"] = datos_formateados

    # --- NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])

    with col_atras:
        if st.button("⬅️ Atrás"):
            guardar_antecedentes() # Se guarda antes de salir
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx > 0:
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()

    with col_guardar:
        if st.button("Guardar registro y continuar"):
            guardar_antecedentes() # Se guarda antes de seguir
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[idx + 1]
                st.rerun()

if __name__ == "__main__":
    render()
