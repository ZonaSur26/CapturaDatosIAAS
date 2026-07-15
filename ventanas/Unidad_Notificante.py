
import streamlit as st

def render():
    st.title("Unidad Notificante")
    st.markdown("---")
    
    # 1. Definición de datos predeterminados para Tlahuac
    tlahuac_data = {
        "Entidad": "CDMX",
        "Jurisdicción": "Tlahuac",
        "CLUES": "DFIST00053",
        "Municipio": "Tlahuac",
        "Localidad": "Tlahuac"
    }

    # 2. Selección de la unidad
    opcion_unidad = st.selectbox(
        "Seleccione la Unidad Notificante:", 
        ["Seleccione...", "Tlahuac", "Otro"]
    )

    # 3. Lógica de habilitación de campos
    if opcion_unidad == "Tlahuac":
        disabled = True
        datos = tlahuac_data
    else:
        disabled = False
        datos = {"Entidad": "", "Jurisdicción": "", "CLUES": "", "Municipio": "", "Localidad": ""}

    # 4. Campo de especificación si es "Otro"
    especificar = None
    if opcion_unidad == "Otro":
        especificar = st.text_input("Especifique el nombre de la unidad:")

    # 5. Formulario de captura
    with st.form("form_unidad"):
        col1, col2 = st.columns(2)
        
        with col1:
            entidad = st.text_input("Entidad", value=datos["Entidad"], disabled=disabled)
            jurisdiccion = st.text_input("Jurisdicción", value=datos["Jurisdicción"], disabled=disabled)
            clues = st.text_input("CLUES", value=datos["CLUES"], disabled=disabled)
        
        with col2:
            municipio = st.text_input("Municipio", value=datos["Municipio"], disabled=disabled)
            localidad = st.text_input("Localidad", value=datos["Localidad"], disabled=disabled)
        
        # Botón de guardado
        submit = st.form_submit_button("Guardar Registro")
        
        if submit:
            if opcion_unidad == "Seleccione...":
                st.error("Por favor, seleccione una unidad válida antes de guardar.")
            elif opcion_unidad == "Otro" and not especificar:
                st.warning("El campo 'Especifique' es obligatorio si seleccionó 'Otro'.")
            else:
                # Aquí se integrará la lógica de guardado (ej. gspread)
                nombre_final = especificar if opcion_unidad == "Otro" else "Tlahuac"
                st.success(f"Datos de la unidad '{nombre_final}' guardados exitosamente.")
                
                # Ejemplo de visualización de los datos capturados
                datos_capturados = {
                    "Unidad": nombre_final,
                    "Entidad": entidad,
                    "Jurisdicción": jurisdiccion,
                    "CLUES": clues,
                    "Municipio": municipio,
                    "Localidad": localidad
                }
                st.json(datos_capturados)
