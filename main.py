import streamlit as st
from ventanas import Unidad_Notificante, Identificacion_paciente, Hospitalizacion # Importamos el nuevo archivo

st.set_page_config(page_title="EpidemioManager", layout="wide")

# Inicializamos la página actual si no existe
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Unidad Notificante"

paginas = {
    "Unidad Notificante": Unidad_Notificante,
    "Identificación Paciente": Identificacion_paciente,
    "Datos de hospitalización": Hospitalizacion # Añadido aquí
}

def main():
    st.sidebar.title("Menú Principal")
    
    opciones = list(paginas.keys())
    seleccion = st.sidebar.radio(
        "Navegación", 
        opciones, 
        index=opciones.index(st.session_state.pagina_actual)
    )
    
    st.session_state.pagina_actual = seleccion
    
    # Invocamos la función 'render' del módulo seleccionado
    pagina = paginas[seleccion]
    pagina.render()

if __name__ == "__main__":
    main()
