import streamlit as st
from ventanas import Unidad_Notificante, Identificacion_paciente

st.set_page_config(page_title="EpidemioManager", layout="wide")

# Mapeamos el nombre que verá el usuario con el módulo importado
paginas = {
    "Unidad Notificante": Unidad_Notificante,
    "Identificación Paciente": Identificacion_paciente
}

def main():
    st.sidebar.title("Menú Principal")
    # El radio button ahora mostrará ambas opciones
    seleccion = st.sidebar.radio("Navegación", list(paginas.keys()))
    
    # Invocamos la función 'render' del módulo seleccionado
    pagina = paginas[seleccion]
    pagina.render()

if __name__ == "__main__":
    main()
