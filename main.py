import streamlit as st
import ventanas.1Unidad_Notificante as unidad_notificante

st.set_page_config(page_title="EpidemioManager", layout="wide")

# Diccionario de navegación
paginas = {
    "Unidad Notificante": unidad_notificante
}

def main():
    st.sidebar.title("Menú Principal")
    seleccion = st.sidebar.radio("Navegación", list(paginas.keys()))
    
    # Llamamos a la función 'render' del módulo seleccionado
    pagina = paginas[seleccion]
    pagina.render()

if __name__ == "__main__":
    main()
