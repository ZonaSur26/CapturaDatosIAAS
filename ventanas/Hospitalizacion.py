
import streamlit as st

def render():
    st.title("Datos de Hospitalización y Egreso")

    # --- INFORMACIÓN DE INGRESO ---
    st.subheader("Información de Ingreso")
    c1, c2 = st.columns(2)
    with c1:
        fecha_ingreso = st.date_input("Fecha de ingreso")
        servicio = st.selectbox("Servicio de ingreso", ["Urgencias", "Medicina Interna", "Cirugía", "Ginecología", "Pediatría", "UCI"], index=None)
    with c2:
        motivo_ingreso = st.text_area("Motivo de ingreso")

    # --- INFORMACIÓN DE EGRESO ---
    st.subheader("Información de Egreso")
    c3, c4 = st.columns(2)
    with c3:
        fecha_egreso = st.date_input("Fecha de egreso", value=None)
        condicion_egreso = st.selectbox("Condición al egreso", ["Mejoría", "Alta voluntaria", "Defunción", "Traslado"], index=None)
    with c4:
        diagnostico_egreso = st.text_area("Diagnóstico final")

    # --- ACCIÓN ---
    if st.button("Guardar datos de hospitalización"):
        st.session_state.datos_hospitalizacion = {
            "Fecha_Ingreso": str(fecha_ingreso),
            "Servicio": servicio,
            "Motivo": motivo_ingreso,
            "Fecha_Egreso": str(fecha_egreso),
            "Condicion": condicion_egreso,
            "Diagnostico": diagnostico_egreso
        }
        st.success("Datos de hospitalización guardados correctamente.")
