import streamlit as st
from ventanas import Unidad_Notificante, Identificacion_paciente, Hospitalizacion, Antecedentes, IAAS

st.set_page_config(page_title="EpidemioManager", layout="wide")

if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Unidad Notificante"

paginas = {
    "Unidad Notificante": Unidad_Notificante,
    "Identificación Paciente": Identificacion_paciente,
    "Datos de hospitalización": Hospitalizacion,
    "Antecedentes Personales": Antecedentes,
    "IAAS y Factores de Riesgo": IAAS,
}

def main():
    st.sidebar.title("Menú Principal")
    opciones = list(paginas.keys())
    
    seleccion = st.sidebar.radio(
        "Navegación", 
        opciones, 
        index=opciones.index(st.session_state.pagina_actual)
    )
    
    if st.session_state.pagina_actual != seleccion:
        st.session_state.pagina_actual = seleccion
        st.rerun()
    
    paginas[seleccion].render()

if __name__ == "__main__":
    main()
