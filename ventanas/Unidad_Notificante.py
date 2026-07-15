import streamlit as st

def render():
    st.title("Unidad Notificante")
    st.markdown("---")

    # CSS para el botón rojo y para resaltar campos bloqueados
    st.markdown("""
        <style>
        /* Estilo para el botón rojo */
        div.stButton > button:first-child {
            background-color: #FF4B4B;
            color: white;
            border: none;
        }
        div.stButton > button:first-child:hover {
            background-color: #FF2B2B;
            color: white;
        }
        
        /* Estilo para campos deshabilitados (Tlahuac) */
        input:disabled {
            background-color: #FFF3E0 !important; /* Fondo naranja suave */
            color: #E65100 !important;           /* Texto naranja oscuro */
            border: 2px solid #FF9800 !important; /* Borde naranja visible */
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. Definición de datos
    tlahuac_data = {
        "Entidad": "CDMX", "Jurisdicción": "Tlahuac", 
        "CLUES": "DFIST00053", "Municipio": "Tlahuac", "Localidad": "Tlahuac"
    }

    # 2. Selección
    opcion_unidad = st.selectbox("Seleccione la Unidad Notificante:", ["Seleccione...", "Tlahuac", "Otro"])
    
    # 3. Lógica de habilitación
    disabled = (opcion_unidad == "Tlahuac" or opcion_unidad == "Seleccione...")
    
    if opcion_unidad == "Tlahuac":
        datos = tlahuac_data
    else:
        datos = {"Entidad": "", "Jurisdicción": "", "CLUES": "", "Municipio": "", "Localidad": ""}

    with st.form("form_unidad"):
        col1, col2 = st.columns(2)
        with col1:
            entidad = st.text_input("Entidad", value=datos["Entidad"], disabled=disabled)
            jurisdiccion = st.text_input("Jurisdicción", value=datos["Jurisdicción"], disabled=disabled)
            clues = st.text_input("CLUES", value=datos["CLUES"], disabled=disabled)
        with col2:
            municipio = st.text_input("Municipio", value=datos["Municipio"], disabled=disabled)
            localidad = st.text_input("Localidad", value=datos["Localidad"], disabled=disabled)
        
        submit = st.form_submit_button("Guardar Registro y Continuar")
        
        if submit:
            if opcion_unidad == "Seleccione...":
                st.error("Por favor, selecciona una unidad.")
            else:
                st.session_state.datos_unidad = {
                    "Entidad": entidad, "Jurisdicción": jurisdiccion, 
                    "CLUES": clues, "Municipio": municipio, "Localidad": localidad
                }
                st.success("Datos guardados correctamente.")
