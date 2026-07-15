import streamlit as st

def render():
    st.title("Antecedentes Personales Patológicos")
    st.subheader("Seleccione los antecedentes presentes")

    # Lista de antecedentes
    antecedentes_lista = [
        "PREMATUREZ", "BAJO PESO AL NACER", "DIABETES MELLITUS", 
        "HIPERTENSIÓN ARTERIAL SISTÉMICA", "SOBREPESO/OBESIDAD", "TABAQUISMO",
        "DESNUTRICIÓN", "ENFERMEDAD RENAL CRÓNICA", "EPOC", 
        "VIH/SIDA", "INMUNOSUPRESIÓN", "CANCER"
    ]

    # Creamos un diccionario para guardar los valores
    antecedentes_seleccionados = {}

    # Layout en 2 columnas para que sea amigable y compacto
    col1, col2 = st.columns(2)
    
    # Dividimos la lista para las dos columnas
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
        # Convertimos a mayúsculas en tiempo real con on_change o simplemente al procesar
        # Aquí usamos un text_input normal y lo convertimos al guardar
        otro_antecedente = st.text_input("Especifique el otro antecedente:").upper()
        antecedentes_seleccionados["OTRO"] = otro_antecedente

    # --- ACCIÓN ---
    if st.button("Guardar registro y continuar"):
        # Estructuramos los datos para que sea fácil enviarlos a Google Sheets
        # Si el checkbox está marcado, es "SÍ", de lo contrario "NO"
        datos_formateados = {
            k: ("SÍ" if v is True else "NO") if k != "OTRO" else v 
            for k, v in antecedentes_seleccionados.items()
        }
        
        st.session_state.datos_antecedentes = datos_formateados
        st.success("Antecedentes guardados.")
        
        # st.session_state.pagina_actual = "Siguiente Ventana"
        # st.rerun()
