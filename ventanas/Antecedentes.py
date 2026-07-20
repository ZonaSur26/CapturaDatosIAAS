import streamlit as st
import sys

def render():
    st.title("Antecedentes Personales Patológicos")
    st.subheader("Seleccione los antecedentes presentes")

    # Lista de antecedentes
    antecedentes_lista = [
        "PREMATUREZ", "BAJO PESO AL NACER", "DIABETES MELLITUS", 
        "HIPERTENSIÓN ARTERIAL SISTÉMICA", "SOBREPESO", "OBESIDAD" "TABAQUISMO",
        "DESNUTRICIÓN", "ENFERMEDAD RENAL CRÓNICA", "EPOC", 
        "VIH/SIDA", "INMUNOSUPRESIÓN", "CANCER"
    ]

    # Creamos un diccionario para guardar los valores
    antecedentes_seleccionados = {}

    # Layout en 2 columnas
    col1, col2 = st.columns(2)
    
    mitad = len(antecedentes_lista) // 2
    
    with col1:
        for item in antecedentes_lista[:mitad]:
            antecedentes_seleccionados[item] = st.checkbox(item)
    with col2:
        for item in antecedentes_lista[mitad:]:
            antecedentes_seleccionados[item] = st.checkbox(item)

    # --- CAMPO "OTRO" ---
    st.markdown("---")
    es_otro = st.checkbox("OTRO")
    otro_antecedente = ""
    if es_otro:
        otro_antecedente = st.text_input("Especifique el otro antecedente:").upper()
    
    # --- ACCIÓN DE GUARDADO Y NAVEGACIÓN ---
    if st.button("Guardar registro y continuar"):
        # Procesamiento de datos
        datos_formateados = {
            k: ("SÍ" if v is True else "NO") for k, v in antecedentes_seleccionados.items()
        }
        datos_formateados["OTRO"] = otro_antecedente if es_otro else "NO APLICA"
        
        # Guardado centralizado
        st.session_state.datos_completos["Antecedentes"] = datos_formateados
        
        # Navegación automática segura
        main_module = sys.modules['main']
        ORDEN = main_module.ORDEN
        indice = ORDEN.index(st.session_state.pagina_actual)
        
        if indice < len(ORDEN) - 1:
            st.session_state.pagina_actual = ORDEN[indice + 1]
            st.success("Antecedentes guardados. Redirigiendo...")
            st.rerun()

if __name__ == "__main__":
    render()
