import streamlit as st

# --- IMPORTACIONES ---
from ventanas.Unidad_Notificante import render as render_unidad
from ventanas.Identificacion_paciente import render as render_paciente
from ventanas.Hospitalizacion import render as render_hosp
from ventanas.Antecedentes import render as render_ante
from ventanas.IAAS import render as render_iaas
from ventanas.Microbiologia import render as render_micro
from ventanas.Polimicrobiana import render as render_poli
from ventanas.Tratamiento import render as render_tratamiento
from ventanas.Deteccion import render as render_deteccion

# --- CONFIGURACIÓN Y ESTADO ---
ORDEN = [
    "Unidad Notificante", "Identificación Paciente", "Datos de hospitalización",
    "Antecedentes Personales", "IAAS y Factores de Riesgo", "Diagnóstico Microbiológico",
    "Infección Polimicrobiana", "Tratamiento de IAAS", "Detección y Notificación"
]

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

st.set_page_config(page_title="EpidemioManager", layout="wide")

# Inicialización
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = ORDEN[0]

if 'datos_completos' not in st.session_state:
    st.session_state.datos_completos = {key: {} for key in ORDEN}

def main():
    st.sidebar.title("EpidemioManager")
    
    # 1. Navegación Lateral (Sincronizada)
    seleccion = st.sidebar.radio(
        "Menú de Navegación", 
        ORDEN, 
        index=ORDEN.index(st.session_state.pagina_actual)
    )
    
    # Actualizar estado si cambia el menú lateral
    if seleccion != st.session_state.pagina_actual:
        st.session_state.pagina_actual = seleccion
        st.rerun()

    # 2. Área de Navegación (Botón Atrás global)
    idx = ORDEN.index(st.session_state.pagina_actual)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if idx > 0:
            if st.button("⬅️ Atrás"):
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()
    
    # 3. Renderizado de la ventana activa
    st.divider()
    paginas[st.session_state.pagina_actual]()

if __name__ == "__main__":
    main()
