import streamlit as st

def render_pestaña1():
    st.header("Unidad Notificante")
    with st.form("form_unidad"):
        nombre_unidad = st.text_input("Nombre de la Unidad")
        clues = st.text_input("CLUES")
        submit = st.form_submit_button("Guardar sección")
        
    if submit:
        st.success(f"Datos de {nombre_unidad} guardados.")
