import streamlit as st

def render():
    st.title("Unidad Notificante")
    st.markdown("---")

    # CSS para el botón rojo
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #FF4B4B;
            color: white;
            border: none;
        }
        div.stButton > button:first-child:hover {
            background-color: #FF2B2B;
            color: white;
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
    # Si es "Seleccione..." o "Otro", deshabilitamos por defecto (si es Otro, el usuario escribirá en un campo nuevo si quieres, o dejamos los campos bloqueados hasta que elija)
    # Aquí: Deshabilitar si es "Seleccione..." o si es "Tlahuac" (para que no editen los datos precargados)
    if opcion_unidad == "Tlahuac":
        disabled = True
        datos = tlahuac_data
    elif opcion_unidad == "Seleccione...":
        disabled = True
        datos = {"Entidad": "", "Jurisdicción": "", "CLUES": "", "Municipio": "", "Localidad": ""}
    else: # Caso "Otro"
        disabled = False
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
        
        # El botón solo debe ser funcional si hay una selección válida
        submit = st.form_submit_button("Guardar Registro y Continuar")
        
        if submit:
            if opcion_unidad == "Seleccione...":
                st.error("Por favor, selecciona una unidad antes de continuar.")
            else:
                st.session_state.datos_unidad = {
                    "Entidad": entidad, "Jurisdicción": jurisdiccion, 
                    "CLUES": clues, "Municipio": municipio, "Localidad": localidad
                }
                st.success("Registro guardado. Procediendo...")
