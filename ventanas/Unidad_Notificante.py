import streamlit as st
from datetime import datetime

def render():
    st.title("Unidad Notificante")
    st.markdown("---")

    # --- FECHA Y MES AUTOMÁTICOS ---
    if 'fecha_captura' not in st.session_state:
        st.session_state.fecha_captura = datetime.now().strftime("%d/%m/%Y")
    
    mes_actual_idx = datetime.now().month - 1
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    # --- CAMPOS INICIALES ---
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Fecha de captura:", value=st.session_state.fecha_captura, disabled=True)
    with c2:
        mes_captura = st.selectbox("Mes de captura:", meses, index=mes_actual_idx)

    # --- LÓGICA DE UNIDAD ---
    tlahuac_data = {"Entidad": "CDMX", "Jurisdicción": "Tlahuac", "CLUES": "DFIST00053", "Municipio": "Tlahuac", "Localidad": "Tlahuac"}
    opcion_unidad = st.selectbox("Seleccione la Unidad Notificante:", ["Seleccione...", "Tlahuac", "Otro"])
    
    is_tlahuac = (opcion_unidad == "Tlahuac")
    datos = tlahuac_data if is_tlahuac else {"Entidad": "", "Jurisdicción": "", "CLUES": "", "Municipio": "", "Localidad": ""}

    with st.form("form_unidad"):
        col1, col2 = st.columns(2)
        with col1:
            entidad = st.text_input("Entidad", value=datos["Entidad"], disabled=is_tlahuac)
            jurisdiccion = st.text_input("Jurisdicción", value=datos["Jurisdicción"], disabled=is_tlahuac)
            clues = st.text_input("CLUES", value=datos["CLUES"], disabled=is_tlahuac)
        with col2:
            municipio = st.text_input("Municipio", value=datos["Municipio"], disabled=is_tlahuac)
            localidad = st.text_input("Localidad", value=datos["Localidad"], disabled=is_tlahuac)
        
        submit = st.form_submit_button("Guardar Registro y Continuar")
        
        if submit:
            # --- VALIDACIÓN DE CAMPOS ---
            campos_vacios = [
                field for field, val in [("Entidad", entidad), ("Jurisdicción", jurisdiccion), 
                                         ("CLUES", clues), ("Municipio", municipio), ("Localidad", localidad)]
                if not val.strip()
            ]
            
            if opcion_unidad == "Seleccione...":
                st.error("Por favor, selecciona una unidad.")
            elif campos_vacios:
                st.error(f"Faltan datos obligatorios: {', '.join(campos_vacios)}")
            else:
                # Guardado en el contenedor global
                st.session_state.datos_completos["Unidad"] = {
                    "Fecha": st.session_state.fecha_captura,
                    "Mes": mes_captura,
                    "Entidad": entidad, 
                    "Jurisdicción": jurisdiccion, 
                    "CLUES": clues, 
                    "Municipio": municipio, 
                    "Localidad": localidad
                }
                
                # --- NAVEGACIÓN AUTOMÁTICA ---
                # Importamos ORDEN del main o lo definimos aquí para avanzar al siguiente
                from main import ORDEN 
                indice_actual = ORDEN.index(st.session_state.pagina_actual)
                if indice_actual < len(ORDEN) - 1:
                    st.session_state.pagina_actual = ORDEN[indice_actual + 1]
                    st.success("Datos guardados. Redirigiendo...")
                    st.rerun()

if __name__ == "__main__":
    render()
