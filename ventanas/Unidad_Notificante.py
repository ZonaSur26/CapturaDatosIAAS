import streamlit as st

def render():
    st.title("Unidad Notificante")
    st.markdown("---")

    # Inyección de CSS para botón rojo
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #FF4B4B;
            color: white;
        }
        div.stButton > button:first-child:hover {
            background-color: #FF2B2B;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    # ... (Lógica de selección y datos igual a la anterior) ...
    tlahuac_data = {"Entidad": "CDMX", "Jurisdicción": "Tlahuac", "CLUES": "DFIST00053", "Municipio": "Tlahuac", "Localidad": "Tlahuac"}
    opcion_unidad = st.selectbox("Seleccione la Unidad Notificante:", ["Seleccione...", "Tlahuac", "Otro"])
    
    # Lógica de estados (disabled/datos) igual a la anterior...
    disabled = (opcion_unidad == "Tlahuac")
    datos = tlahuac_data if opcion_unidad == "Tlahuac" else {"Entidad": "", "Jurisdicción": "", "CLUES": "", "Municipio": "", "Localidad": ""}

    with st.form("form_unidad"):
        # ... (Campos de entrada igual a la anterior) ...
        col1, col2 = st.columns(2)
        with col1:
            entidad = st.text_input("Entidad", value=datos["Entidad"], disabled=disabled)
            jurisdiccion = st.text_input("Jurisdicción", value=datos["Jurisdicción"], disabled=disabled)
        with col2:
            clues = st.text_input("CLUES", value=datos["CLUES"], disabled=disabled)
            municipio = st.text_input("Municipio", value=datos["Municipio"], disabled=disabled)
        
        # Botón personalizado
        submit = st.form_submit_button("Guardar Registro y Continuar")
        
        if submit:
            # Aquí irá tu lógica de gspread para guardar
            st.session_state.datos_unidad = {"Entidad": entidad, "Jurisdicción": jurisdiccion} # Guardar en estado
            st.success("Registro guardado. Procediendo a la siguiente sección...")
            
            # Navegación automática a la siguiente ventana
            # st.session_state.pagina_actual = "Siguiente Ventana"
            # st.rerun()
