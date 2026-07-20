import streamlit as st
from datetime import datetime
from config import ORDEN  # Importa ORDEN desde config.py

def render():
    st.title("Unidad Notificante")
    st.markdown("---")

    # 1. ASEGURAR QUE EXISTE EL DICCIONARIO GLOBAL EN SESSION_STATE
    if "datos_completos" not in st.session_state:
        st.session_state.datos_completos = {"Unidad": {}, "Paciente": {}}

    guardados = st.session_state.datos_completos.get("Unidad", {})
    
    # --- FECHA Y MES ---
    if 'fecha_captura' not in st.session_state:
        st.session_state.fecha_captura = datetime.now().strftime("%d/%m/%Y")
    
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    # Recupera el mes guardado o el actual
    mes_guardado = guardados.get("Mes", meses[datetime.now().month - 1])
    mes_idx = meses.index(mes_guardado) if mes_guardado in meses else datetime.now().month - 1

    c1, c2 = st.columns(2)
    with c1:
        # Se guarda la fecha de captura en formato dd/mm/aaaa
        fecha_display = guardados.get("Fecha", st.session_state.fecha_captura)
        st.text_input("Fecha de captura:", value=fecha_display, disabled=True)
    with c2:
        mes_captura = st.selectbox("Mes de captura:", meses, index=mes_idx)

    # --- LÓGICA DE SELECCIÓN DE UNIDAD ---
    opcion_guardada = guardados.get("Unidad_Select", "Seleccione...")
    opciones = ["Seleccione...", "Tlahuac", "Otro"]
    idx_unidad = opciones.index(opcion_guardada) if opcion_guardada in opciones else 0
    
    opcion_unidad = st.selectbox("Seleccione la Unidad Notificante:", opciones, index=idx_unidad)
    
    # Identificar si es Tlahuac para el autocompletado
    is_tlahuac = (opcion_unidad == "Tlahuac")
    
    # --- DETERMINAR VALORES POR DEFECTO ---
    # Si ya hay datos guardados en el estado de la sesión, los usamos.
    # Si no hay nada guardado pero seleccionó Tlahuac, precargamos sus datos.
    if guardados.get("Unidad_Select") == opcion_unidad:
        # Si la opción actual coincide con lo guardado, mantenemos lo guardado
        val_entidad = guardados.get("Entidad", "")
        val_jurisdiccion = guardados.get("Jurisdicción", "")
        val_clues = guardados.get("CLUES", "")
        val_municipio = guardados.get("Municipio", "")
        val_localidad = guardados.get("Localidad", "")
    elif is_tlahuac:
        # Si es Tlahuac nuevo (sin guardar previo), precargamos
        val_entidad = "CDMX"
        val_jurisdiccion = "Tlahuac"
        val_clues = "DFIST00053"
        val_municipio = "Tlahuac"
        val_localidad = "Tlahuac"
    else:
        # Si es "Otro" o "Seleccione...", iniciamos vacío
        val_entidad = ""
        val_jurisdiccion = ""
        val_clues = ""
        val_municipio = ""
        val_localidad = ""

    # --- FORMULARIO DE CAPTURA ---
    with st.form("form_unidad"):
        col1, col2 = st.columns(2)
        with col1:
            entidad = st.text_input("Entidad", value=val_entidad, disabled=is_tlahuac)
            jurisdiccion = st.text_input("Jurisdicción", value=val_jurisdiccion, disabled=is_tlahuac)
            clues = st.text_input("CLUES", value=val_clues, disabled=is_tlahuac)
        with col2:
            municipio = st.text_input("Municipio", value=val_municipio, disabled=is_tlahuac)
            localidad = st.text_input("Localidad", value=val_localidad, disabled=is_tlahuac)
        
        submit = st.form_submit_button("💾 Guardar registro y continuar")
        
        if submit:
            if opcion_unidad == "Seleccione...":
                st.error("⚠️ Por favor, seleccione una Unidad Notificante válida antes de continuar.")
            else:
                # --- ASIGNACIÓN DE VARIABLES EXACTAS PARA UTILS.PY ---
                st.session_state.datos_completos["Unidad"] = {
                    "Fecha": fecha_display,          # Columna A
                    "Mes": mes_captura,              # Variable interna de control
                    "Unidad_Select": opcion_unidad,  # Columna B
                    "Entidad": entidad,              # Columna C
                    "Municipio": municipio,          # Columna D
                    "Jurisdicción": jurisdiccion,    # Columna E
                    "Localidad": localidad,          # Columna F
                    "CLUES": clues                   # Columna G
                }
                
                # Avanzar de página según tu archivo config.py
                try:
                    idx = ORDEN.index(st.session_state.pagina_actual)
                    st.session_state.pagina_actual = ORDEN[idx + 1]
                    st.rerun()
                except (ValueError, IndexError):
                    st.error("Error en la navegación. Verifica el archivo config.py")

if __name__ == "__main__":
    render()
