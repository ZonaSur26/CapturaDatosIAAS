import streamlit as st

# La sintaxis correcta usando paréntesis debe separar cada elemento con una coma
from ventanas import (
    Unidad_Notificante,
    Identificacion_paciente,
    Hospitalizacion,
    Antecedentes,
    IAAS
)

st.set_page_config(page_title="EpidemioManager", layout="wide")

# Inicializamos la página actual si no existe
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Unidad Notificante"

# Diccionario de navegación
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
    
    # Navegación mediante radio button en el sidebar
    seleccion = st.sidebar.radio(
        "Navegación", 
        opciones, 
        index=opciones.index(st.session_state.pagina_actual)
    )
    
    # Actualizamos el estado solo si hubo un cambio
    if st.session_state.pagina_actual != seleccion:
        st.session_state.pagina_actual = seleccion
        st.rerun()
    
    # Renderizado dinámico de la página seleccionada
    pagina = paginas[seleccion]
    pagina.render()

if __name__ == "__main__":
    main()
