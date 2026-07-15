import streamlit as st

def render():
    st.title("Identificación del Paciente")
    st.markdown("---")
    
    # Verificación de flujo: ¿Ya se capturó la unidad?
    if 'datos_unidad' not in st.session_state:
        st.warning("⚠️ Primero debes completar la sección de 'Unidad Notificante'.")
        return
    else:
        st.info(f"Unidad seleccionada: {st.session_state.datos_unidad.get('Jurisdicción')}")

    with st.form("form_paciente"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre del Paciente")
            expediente = st.text_input("Número de Expediente")
            fecha_nacimiento = st.date_input("Fecha de Nacimiento")
            
        with col2:
            sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
            curp = st.text_input("CURP")
            
        submit = st.form_submit_button("Guardar Paciente y Continuar")
        
        if submit:
            st.session_state.datos_paciente = {
                "Nombre": nombre,
                "Expediente": expediente,
                "CURP": curp
            }
            st.success("Información del paciente guardada.")
