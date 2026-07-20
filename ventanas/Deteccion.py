import streamlit as st
import pandas as pd
import io
import sys
from config import ORDEN

# Función auxiliar para convertir a mayúsculas
def to_upper(key):
    if st.session_state.get(key):
        st.session_state[key] = st.session_state[key].upper()

def render():
    st.title("Detección y Notificación de la IAAS")
    
    # --- 0. RECUPERACIÓN DE ESTADOS PREVIOS ---
    d = st.session_state.datos_completos.get("Deteccion", {})

    # --- APARTADO 1: ¿QUIÉN DETECTÓ LA IAAS? ---
    st.subheader("Personal de Notificación")
    with st.container(border=True):
        cols = st.columns(3)
        opciones = ["MÉDICO TRATANTE", "MÉDICO DE LA UVEH", "LABORATORIO", "CLÍNICA DE HERIDAS", "HEMODIÁLISIS", "ENFERMERÍA", "ENFERMERÍA UVEH", "INHALOTERÁPIA", "CLÍNICA DE CATETER"]
        seleccionados = {op: cols[i % 3].checkbox(op, key=f"check_{i}", value=d.get("Fuentes", {}).get(op, False)) for i, op in enumerate(opciones)}
        otro = st.checkbox("OTRO", key="check_otro", value=d.get("Otro_Check", False))
        
        if otro:
            st.text_input("Especifique otro origen:", key="k_esp_otro", value=d.get("Espec_Otro", ""), on_change=lambda: to_upper("k_esp_otro"))

    # --- APARTADO 2: RESPONSABLES ---
    st.subheader("Responsables")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.text_input("RESPONSABLE DE LA DETECCIÓN", key="k_resp_det", value=d.get("Resp_Deteccion", ""), on_change=lambda: to_upper("k_resp_det"))
        c2.text_input("RESPONSABLE DE LA CAPTURA", key="k_resp_cap", value=d.get("Resp_Captura", ""), on_change=lambda: to_upper("k_resp_cap"))
        c3.text_input("RESPONSABLE DE LA UVEH", key="k_resp_uveh", value=d.get("Resp_UVEH", ""), on_change=lambda: to_upper("k_resp_uveh"))

    # --- APARTADO 3: UNIDAD DE DETECCIÓN ---
    st.subheader("Unidad de Detección")
    fue_otra_unidad = st.radio("¿LA IAAS FUE ADQUIRIDA EN OTRA UNIDAD DE ATENCIÓN?", ["No", "Sí"], key="k_otra_unidad", index=["No", "Sí"].index(d.get("Otra_Unidad", "No")) if d.get("Otra_Unidad") in ["No", "Sí"] else None, horizontal=True)

    if fue_otra_unidad == "Sí":
        with st.container(border=True):
            st.text_input("NOMBRE DE LA UNIDAD DE DONDE PROVIENE LA IAAS", key="k_nom_unidad", value=d.get("Nombre_Unidad", ""), on_change=lambda: to_upper("k_nom_unidad"))
            estados = ["Aguascalientes", "Baja California", "CDMX", "Jalisco", "Nuevo León", "Tamaulipas", "Veracruz", "Zacatecas"]
            st.selectbox("ESTADO DE DONDE PROVIENE LA IAAS", estados, key="k_est_unidad", index=estados.index(d.get("Estado_Unidad")) if d.get("Estado_Unidad") in estados else None)

    # --- FUNCIÓN DE GUARDADO ---
    def guardar():
        st.session_state.datos_completos["Deteccion"] = {
            "Fuentes": {op: st.session_state.get(f"check_{i}", False) for i, op in enumerate(opciones)},
            "Otro_Check": st.session_state.get("check_otro", False),
            "Espec_Otro": st.session_state.get("k_esp_otro", ""),
            "Resp_Deteccion": st.session_state.get("k_resp_det", ""),
            "Resp_Captura": st.session_state.get("k_resp_cap", ""),
            "Resp_UVEH": st.session_state.get("k_resp_uveh", ""),
            "Otra_Unidad": st.session_state.get("k_otra_unidad", "No"),
            "Nombre_Unidad": st.session_state.get("k_nom_unidad", ""),
            "Estado_Unidad": st.session_state.get("k_est_unidad", "")
        }

    # --- NAVEGACIÓN Y ACCIONES ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])
    
    with col_atras:
        if st.button("⬅️ Atrás"):
            guardar()
            idx = ORDEN.index(st.session_state.pagina_actual)
            st.session_state.pagina_actual = ORDEN[idx - 1]
            st.rerun()

    with col_guardar:
        if st.button("💾 Guardar y Capturar"):
            if not st.session_state.get("k_resp_det") or not st.session_state.get("k_resp_cap"):
                st.error("⚠️ Faltan datos obligatorios (Responsables).")
            else:
                st.warning("¿Los datos son correctos?")
                c_si, c_no = st.columns(2)
                if c_si.button("✅ Sí, guardar y generar"):
                    guardar()
                    # Generación de Excel
                    df = pd.json_normalize(st.session_state.datos_completos)
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name="IAAS_Reporte")
                    st.session_state.reporte = buffer.getvalue()
                    
                    # Marcamos que el proceso fue exitoso
                    st.session_state.captura_exitosa = True
                    st.rerun()

    # --- Lógica de visualización del éxito ---
    if st.session_state.get("captura_exitosa"):
        st.balloons()
        st.success("¡Datos capturados y guardados con éxito!")
        # Limpiamos la bandera para que no se repita en futuras interacciones
        st.session_state.captura_exitosa = False
if __name__ == "__main__":
    render()
