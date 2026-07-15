import streamlit as st
from ventanas import Unidad_Notificante, Identificacion_paciente, Hospitalizacion, Antecedentes

st.set_page_config(page_title="EpidemioManager", layout="wide")

# Inicializamos la página actual si no existe
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Unidad Notificante"

# Diccionario de navegación actualizado
paginas = {
    "Unidad Notificante": Unidad_Notificante,
    "Identificación Paciente": Identificacion_paciente,
    "Datos de hospitalización": Hospitalizacion,
    "Antecedentes": Antecedentes
}

def main():
    st.sidebar.title("Menú Principal")
    
    opciones = list(paginas.keys())
    # Usamos 'index' para controlar qué opción está seleccionada según el session_state
    seleccion = st.sidebar.radio(
        "Navegación", 
        opciones, 
        index=opciones.index(st.session_state.pagina_actual)
    )
    
    # Actualizamos el estado si el usuario cambia manualmente en el menú
    if st.session_state.pagina_actual != seleccion:
        st.session_state.pagina_actual = seleccion
        st.rerun()
    
    # Invocamos la función 'render' del módulo seleccionado
    pagina = paginas[seleccion]
    pagina.render()

if __name__ == "__main__":
    main()
