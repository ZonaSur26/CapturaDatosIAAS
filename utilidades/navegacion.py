import streamlit as st
from main import ORDEN 

def boton_navegacion(nombre_pagina_actual):
    st.divider()
    # Dos columnas: una para atrás, otra para guardar y continuar
    col_atras, col_guardar = st.columns([1, 4])
    
    idx = ORDEN.index(nombre_pagina_actual)
    
    with col_atras:
        if idx > 0:
            if st.button("⬅️ Atrás"):
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()
                
    with col_guardar:
        if st.button("💾 Guardar y continuar"):
            # Lógica de guardado silencioso aquí
            if idx < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[idx + 1]
                st.rerun()
