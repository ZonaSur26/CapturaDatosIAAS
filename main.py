import streamlit as st
# Ahora importamos el archivo con su nombre correcto
from ventanas import Unidad_Notificante

st.set_page_config(page_title="EpidemioManager", layout="wide")

# Mapeamos el nombre que verá el usuario con el módulo importado
paginas = {
    "Unidad Notificante": Unidad_Notificante
}

def main():
    st.sidebar.title("Menú Principal")
    seleccion = st.sidebar.radio("Navegación", list(paginas.keys()))
    
    # Invocamos la función 'render' definida dentro de Unidad_Notificante.py
    pagina = paginas[seleccion]
    pagina.render()

if __name__ == "__main__":
    main()
