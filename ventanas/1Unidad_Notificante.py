import streamlit as st

def render():
    st.title("Unidad Notificante")
    
    # Definir valores predeterminados para Tlahuac
    tlahuac_data = {
        "Entidad": "CDMX",
        "Jurisdicción": "Tlahuac",
        "CLUES": "DFIST00053",
        "Municipio": "Tlahuac",
        "Localidad": "Tlahuac"
    }

    # Selección de unidad
    opcion_unidad = st.selectbox("Unidad", ["Seleccione...", "Tlahuac", "Otro"])

    # Lógica para habilitar/deshabilitar y prellenar
    if opcion_unidad == "Tlahuac":
        disabled = True
        datos = tlahuac_data
    else:
        disabled = False
        datos = {"Entidad": "", "Jurisdicción": "", "CLUES": "", "Municipio": "", "Localidad": ""}

    # Campo adicional para "Otro"
    if opcion_unidad == "Otro":
        st.text_input("Especifique el nombre de la unidad:")

    # Formulario de datos
    with st.form("form_unidad"):
        col1, col2 = st.columns(2)
        
        with col1:
            entidad = st.text_input("Entidad", value=datos["Entidad"], disabled=disabled)
            jurisdiccion = st.text_input("Jurisdicción", value=datos["Jurisdicción"], disabled=disabled)
            clues = st.text_input("CLUES", value=datos["CLUES"], disabled=disabled)
        
        with col2:
            municipio = st.text_input("Municipio", value=datos["Municipio"], disabled=disabled)
            localidad = st.text_input("Localidad", value=datos["Localidad"], disabled=disabled)
        
        submit = st.form_submit_button("Guardar Registro")
        
        if submit:
            if opcion_unidad == "Seleccione...":
                st.error("Por favor, seleccione una unidad válida.")
            else:
                st.success(f"Datos de la unidad {opcion_unidad} guardados correctamente.")
                # Aquí conectarás tu lógica de gspread o almacenamiento posteriormente
