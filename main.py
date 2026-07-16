import streamlit as st

# Importamos directamente porque están en la misma carpeta
import Unidad_Notificante
import Identificacion_paciente
import Hospitalizacion
import Antecedentes
import IAAS

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
    
    # Invocamos la función 'render' del módulo
    paginas[seleccion].render()

if __name__ == "__main__":
    main()
