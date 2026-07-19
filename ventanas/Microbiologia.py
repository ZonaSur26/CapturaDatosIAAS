import streamlit as st

def render():
    st.title("Diagnóstico Microbiológico")

    for i in range(1, 5):
        with st.expander(f"Aislamiento {i}"):
            c1, c2 = st.columns(2)
            with c1:
                st.date_input(f"Fecha de toma de muestra {i}", key=f"f_muestra_{i}", value=None)
                st.text_input(f"Sitio anatómico {i}", key=f"sitio_{i}")
            with c2:
                st.text_input(f"Microorganismo {i}", key=f"micro_{i}")
                st.selectbox(f"Resistencia {i}", ["Sensible", "Resistente", "Multirresistente"], index=None, key=f"resistencia_{i}", placeholder="Seleccione...")

    if st.button("Guardar Microbiología"):
        st.success("Datos de microbiología guardados.")
