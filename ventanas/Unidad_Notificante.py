import streamlit as st
from datetime import datetime
from config import ORDEN  # Importa ORDEN desde config.py

def render():
    st.title("Unidad Notificante")
    st.markdown("---")

    # 1. RECUPERAR DATOS GUARDADOS (Si existen)
    guardados = st.session_state.datos_completos.get("Unidad", {})
    
    # --- FECHA Y MES ---
    if 'fecha_captura' not in st.session_state:
        st.session_state.fecha_captura = datetime.now().strftime("%d/%m/%Y")
    
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    # Recupera el mes guardado o el actual
    mes_guardado = guardados.get("Mes", meses[datetime.now().month - 1])
    mes_idx = meses.index(mes_guardado)

    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Fecha de captura:", value=guardados.get("Fecha", st.session_state.fecha_captura), disabled=True)
    with c2:
        mes_captura = st.selectbox("Mes de captura:", meses, index=mes_idx)

    # --- LÓGICA DE UNIDAD ---
    # Recupera la opción de unidad guardada
    opcion_guardada = guardados.get("Unidad_Select", "Seleccione...")
    opciones = ["Seleccione...", "Tlahuac", "Otro"]
    idx_unidad = opciones.index(opcion_guardada) if opcion_guardada in opciones else 0
    
    opcion_unidad = st.selectbox("Seleccione la Unidad Notificante:", opciones, index=idx_unidad)
    
    # Lógica de precarga: si hay datos guardados, úsalos; si no, usa Tlahuac si se seleccionó
    is_tlahuac = (opcion_unidad == "Tlahuac")
    
    # Prioridad: 1. Datos guardados, 2. Datos Tlahuac, 3. Vacío
    datos_precarga = guardados if guardados else ({"Entidad": "CDMX", "Jurisdicción": "Tlahuac", "CLUES": "DFIST00053", "Municipio": "Tlahuac", "Localidad": "Tlahuac"} if is_tlahuac else {"Entidad": "", "Jurisdicción": "", "CLUES": "", "Municipio": "", "Localidad": ""})

    with st.form("form_unidad"):
        col1, col2 = st.columns(2)
        with col1:
            entidad = st.text_input("Entidad", value=datos_precarga.get("Entidad", ""), disabled=is_tlahuac)
            jurisdiccion = st.text_input("Jurisdicción", value=datos_precarga.get("Jurisdicción", ""), disabled=is_tlahuac)
            clues = st.text_input("CLUES", value=datos_precarga.get("CLUES", ""), disabled=is_tlahuac)
        with col2:
            municipio = st.text_input("Municipio", value=datos_precarga.get("Municipio", ""), disabled=is_tlahuac)
            localidad = st.text_input("Localidad", value=datos_precarga.get("Localidad", ""), disabled=is_tlahuac)
        
        submit = st.form_submit_button("Guardar Registro y Continuar")
        
        if submit:
            # --- VALIDACIÓN ---
            st.session_state.datos_completos["Unidad"] = {
                "Fecha": st.session_state.fecha_captura, "Mes": mes_captura, "Unidad_Select": opcion_unidad,
                "Entidad": entidad, "Jurisdicción": jurisdiccion, "CLUES": clues, 
                "Municipio": municipio, "Localidad": localidad
            }
            # Navegación
            idx = ORDEN.index(st.session_state.pagina_actual)
            st.session_state.pagina_actual = ORDEN[idx + 1]
            st.rerun()

if __name__ == "__main__":
    render()
