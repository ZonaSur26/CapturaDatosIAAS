import streamlit as st

def render():
    st.title("Unidad Notificante")
    st.write("Configuración inicial de la unidad.")
    
    # Ejemplo de uso de las librerías que solicitaste
    with st.form("form_unidad"):
        nombre = st.text_input("Nombre de la Unidad")
        submit = st.form_submit_button("Guardar")
        
        if submit:
            st.success(f"Unidad {nombre} registrada.")
