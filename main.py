import streamlit as st
from ventanas.Unidad_Notificante import render as render_unidad
from ventanas.Identificacion_paciente import render as render_paciente
from ventanas.Hospitalizacion import render as render_hosp
from ventanas.Antecedentes import render as render_ante
from ventanas.IAAS import render as render_iaas
from ventanas.Microbiologia import render as render_micro
from ventanas.Polimicrobiana import render as render_poli # <--- NUEVA IMPORTACIÓN

st.set_page_config(page_title="EpidemioManager", layout="wide")

if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Unidad Notificante"

paginas = {
    "Unidad Notificante": render_unidad,
    "Identificación Paciente": render_paciente,
    "Datos de hospitalización": render_hosp,
    "Antecedentes Personales": render_ante,
    "IAAS y Factores de Riesgo": render_iaas,
    "Diagnóstico Microbiológico": render_micro,
    "Infección Polimicrobiana": render_poli, # <--- NUEVA PESTAÑA
}

def main():
    st.sidebar.title("Menú Principal")
    opciones = list(paginas.keys())
    
    seleccion = st.sidebar.radio(
        "Navegación", 
        opciones, 
        index=opciones.index(st.session_state.pagina_actual) if st.session_state.pagina_actual in opciones else 0
    )
    
    if st.session_state.pagina_actual != seleccion:
        st.session_state.pagina_actual = seleccion
        st.rerun()
    
    paginas[seleccion]()

if __name__ == "__main__":
    main()
