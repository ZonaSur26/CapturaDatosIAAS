import streamlit as st
import sys
import os

# Esto añade la carpeta actual al camino de búsqueda de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
    
    # Invocamos la función 'render' del módulo
    paginas[seleccion].render()

if __name__ == "__main__":
    main()
