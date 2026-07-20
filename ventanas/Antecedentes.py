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

    antecedentes_seleccionados = {}

    # Layout en 2 columnas
    col1, col2 = st.columns(2)
    mitad = (len(antecedentes_lista) + 1) // 2
    
    with col1:
        for item in antecedentes_lista[:mitad]:
            antecedentes_seleccionados[item] = st.checkbox(item, key=f"check_{item}")
    with col2:
        for item in antecedentes_lista[mitad:]:
            antecedentes_seleccionados[item] = st.checkbox(item, key=f"check_{item}")

    # --- CAMPO "OTRO" (Debajo de todos los antecedentes) ---
    st.markdown("---")
    es_otro = st.checkbox("OTRO", key="check_otro")
    otro_antecedente = ""
    if es_otro:
        st.text_input(
            "Especifique el otro antecedente:", 
            key="otro_text", 
            on_change=to_upper, 
            args=["otro_text"]
        )
        otro_antecedente = st.session_state.otro_text

    # --- NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])

    with col_atras:
        if st.button("⬅️ Atrás"):
            idx = ORDEN.index(st.session_state.pagina_actual)
            st.session_state.pagina_actual = ORDEN[idx - 1]
            st.rerun()

    with col_guardar:
        if st.button("Guardar registro y continuar"):
            datos_formateados = {k: ("SÍ" if v is True else "NO") for k, v in antecedentes_seleccionados.items()}
            datos_formateados["OTRO"] = otro_antecedente if es_otro else "NO APLICA"
            
            st.session_state.datos_completos["Antecedentes"] = datos_formateados
            
            main_module = sys.modules['main']
            ORDEN = main_module.ORDEN
            indice = ORDEN.index(st.session_state.pagina_actual)
            
            if indice < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[idx + 1] # Nota: Asegúrate de tener idx definido
                st.session_state.pagina_actual = ORDEN[indice + 1]
                st.rerun()

if __name__ == "__main__":
    render()
