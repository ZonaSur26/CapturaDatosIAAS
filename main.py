import streamlit as st
import locale

# --- IMPORTACIONES DE VENTANAS ---
from ventanas.Unidad_Notificante import render as render_unidad
from ventanas.Identificacion_paciente import render as render_paciente
from ventanas.Hospitalizacion import render as render_hosp
from ventanas.Antecedentes import render as render_ante
from ventanas.IAAS import render as render_iaas
from ventanas.Microbiologia import render as render_micro
from ventanas.Polimicrobiana import render as render_poli
from ventanas.Tratamiento import render as render_tratamiento
from ventanas.Deteccion import render as render_deteccion

# --- ORDEN DE NAVEGACIÓN ---
# Definido aquí para que sea la fuente de verdad global
ORDEN = [
    "Unidad Notificante", 
    "Identificación Paciente", 
    "Datos de hospitalización",
    "Antecedentes Personales", 
    "IAAS y Factores de Riesgo", 
    "Diagnóstico Microbiológico",
    "Infección Polimicrobiana", 
    "Tratamiento de IAAS", 
    "Detección y Notificación"
]

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="EpidemioManager", layout="wide")

# Inicialización de estados
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = ORDEN[0]

# Diccionario central para persistir todos tus datos
if 'datos_completos' not in st.session_state:
    st.session_state.datos_completos = {
        "Unidad": {}, "Paciente": {}, "Hosp": {}, "Antecedentes": {}, 
        "IAAS": {}, "Micro": {}, "Poli": {}, "Trata": {}, "Deteccion": {}
    }

# Mapeo de páginas
paginas = {
    "Unidad Notificante": render_unidad,
    "Identificación Paciente": render_paciente,
    "Datos de hospitalización": render_hosp,
    "Antecedentes Personales": render_ante,
    "IAAS y Factores de Riesgo": render_iaas,
    "Diagnóstico Microbiológico": render_micro,
    "Infección Polimicrobiana": render_poli,
    "Tratamiento de IAAS": render_tratamiento,
    "Detección y Notificación": render_deteccion,
}

def main():
    st.sidebar.title("EpidemioManager")
    
    # Navegación lateral
    seleccion = st.sidebar.radio(
        "Menú de Navegación", 
        ORDEN, 
        index=ORDEN.index(st.session_state.pagina_actual)
    )
    
    # Sincronización del estado si el usuario cambia desde el sidebar
    if seleccion != st.session_state.pagina_actual:
        st.session_state.pagina_actual = seleccion
        st.rerun()
    
    # Renderizar la ventana activa
    paginas[seleccion]()

if __name__ == "__main__":
    main()
