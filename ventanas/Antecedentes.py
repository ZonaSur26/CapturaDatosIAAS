import streamlit as st
import sys
from config import ORDEN

def render():
    st.title("Antecedentes Personales Patológicos")
    st.subheader("Seleccione los antecedentes presentes")

    # Lista de antecedentes
    antecedentes_lista = [
        "PREMATUREZ", "BAJO PESO AL NACER", "DIABETES MELLITUS", 
        "HIPERTENSIÓN ARTERIAL SISTÉMICA", "SOBREPESO", "OBESIDAD", "TABAQUISMO",
        "DESNUTRICIÓN", "ENFERMEDAD RENAL CRÓNICA", "EPOC", 
        "VIH/SIDA", "INMUNOSUPRESIÓN", "CANCER"
    ]

    antecedentes_seleccionados = {}

    # --- LAYOUT Y UBICACIÓN DE "OTRO" ---
    col1, col2 = st.columns(2)
    
    # Índice donde está OBESIDAD para colocar OTRO debajo
    # Obesidad está en el índice 5, por lo tanto irá en la columna 2 (col2)
    with col1:
        for item in antecedentes_lista[:6]: # Hasta OBESIDAD inclusive
            antecedentes_seleccionados[item] = st.checkbox(item, key=item)
    
    with col2:
        for item in antecedentes_lista[6:]: # Después de OBESIDAD
            antecedentes_seleccionados[item] = st.checkbox(item, key=item)
        
        # --- CAMPO "OTRO" DEBAJO DE OBESIDAD ---
        st.markdown("---")
        es_otro = st.checkbox("OTRO", key="check_otro")
        otro_antecedente = ""
        if es_otro:
            otro_antecedente = st.text_input("Especifique otro antecedente:", key="txt_otro").upper()

    # --- NAVEGACIÓN Y GUARDADO ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])

    with col_atras:
        if st.button("⬅️ Atrás"):
            idx = ORDEN.index(st.session_state.pagina_actual)
            st.session_state.pagina_actual = ORDEN[idx - 1]
            st.rerun()

    with col_guardar:
        if st.button("Guardar registro y continuar"):
            # Procesamiento de datos
            datos_formateados = {k: ("SÍ" if v is True else "NO") for k, v in antecedentes_seleccionados.items()}
            datos_formateados["OTRO"] = otro_antecedente if es_otro else "NO APLICA"
            
            # Guardado centralizado
            st.session_state.datos_completos["Antecedentes"] = datos_formateados
            
            # Navegación automática
            main_module = sys.modules['main']
            ORDEN = main_module.ORDEN
            indice = ORDEN.index(st.session_state.pagina_actual)
            
            if indice < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[indice + 1]
                st.success("Antecedentes guardados. Redirigiendo...")
                st.rerun()

if __name__ == "__main__":
    render()
