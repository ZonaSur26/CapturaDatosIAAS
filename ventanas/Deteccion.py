import streamlit as st
import pandas as pd
import io
import sys

def render():
    st.title("Detección y Notificación de la IAAS")

    # --- APARTADO 1: ¿QUIÉN DETECTÓ LA IAAS? ---
    st.subheader("Personal de Notificación")
    with st.container(border=True):
        cols = st.columns(3)
        opciones = ["MÉDICO TRATANTE", "MÉDICO DE LA UVEH", "LABORATORIO", "CLÍNICA DE HERIDAS", "HEMODIÁLISIS", "ENFERMERÍA", "ENFERMERÍA UVEH", "INHALOTERÁPIA", "CLÍNICA DE CATETER"]
        seleccionados = {op: cols[i % 3].checkbox(op) for i, op in enumerate(opciones)}
        otro = st.checkbox("OTRO")
        especifica_otro = st.text_input("Especifique otro origen:") if otro else ""

    # --- APARTADO 2: RESPONSABLES ---
    st.subheader("Responsables")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        resp_deteccion = c1.text_input("RESPONSABLE DE LA DETECCIÓN")
        resp_captura = c2.text_input("RESPONSABLE DE LA CAPTURA")
        resp_uveh = c3.text_input("RESPONSABLE DE LA UVEH")

    # --- APARTADO 3: UNIDAD DE DETECCIÓN ---
    st.subheader("Unidad de Detección")
    fue_otra_unidad = st.radio("¿LA IAAS FUE ADQUIRIDA EN OTRA UNIDAD DE ATENCIÓN?", ["No", "Sí"], index=None, horizontal=True)
    nombre_unidad = ""
    estado_unidad = ""

    if fue_otra_unidad == "Sí":
        with st.container(border=True):
            nombre_unidad = st.text_input("NOMBRE DE LA UNIDAD DE DONDE PROVIENE LA IAAS")
            estados = ["Aguascalientes", "Baja California", "CDMX", "Jalisco", "Nuevo León", "Tamaulipas", "Veracruz", "Zacatecas"] # (Añade el resto)
            estado_unidad = st.selectbox("ESTADO DE DONDE PROVIENE LA IAAS", estados, index=None)

    # --- ACCIÓN DE GUARDADO Y EXPORTACIÓN ---
    if st.button("Guardar y Generar Excel"):
        # 1. Consolidar todos los datos de st.session_state.datos_completos
        st.session_state.datos_completos["Deteccion"] = {
            "Fuentes": seleccionados,
            "Resp_Deteccion": resp_deteccion,
            "Resp_Captura": resp_captura,
            "Resp_UVEH": resp_uveh,
            "Otra_Unidad": fue_otra_unidad,
            "Nombre_Unidad": nombre_unidad,
            "Estado_Unidad": estado_unidad
        }
        
        # 2. Convertir el diccionario anidado a un DataFrame plano
        df = pd.json_normalize(st.session_state.datos_completos)
        
        # 3. Preparar archivo en memoria
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="IAAS_Reporte")
        
        st.success("¡Datos guardados y reporte listo!")
        
        # 4. Botón de descarga
        st.download_button(
            label="Descargar Reporte Excel",
            data=buffer.getvalue(),
            file_name="Reporte_IAAS.xlsx",
            mime="application/vnd.ms-excel"
        )

if __name__ == "__main__":
    render()
