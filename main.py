import streamlit as st
# Importamos las funciones de cada pestaña
from tabs.pestaña1 import render_pestaña1
from tabs.pestaña2 import render_pestaña2
from tabs.pestaña3 import render_pestaña3
from tabs.pestaña4 import render_pestaña4
from tabs.pestaña5 import render_pestaña5
from tabs.pestaña6 import render_pestaña6
from tabs.pestaña7 import render_pestaña7
from tabs.pestaña8 import render_pestaña8

st.set_page_config(page_title="Sistema de Vigilancia IAAS", layout="wide")

st.title("Captura de Datos Epidemiológicos")

# Definición de pestañas
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Unidad Notificante", 
    "Datos de identificación", 
    "Datos de hospitalización y egreso", 
    "Antecedentes personales patológicos", 
    "Datos de la IAAS y sus factores de riesgo", 
    "Diagnóstico microbiológico", 
    "Tratamiento Instaurado", 
    "Detección y notificación"
])

# Renderizado de cada módulo
with tab1:
    render_pestaña1()
with tab2:
    render_pestaña2()
with tab3:
    render_pestaña3()
with tab4:
    render_pestaña4()
with tab5:
    render_pestaña5()
with tab6:
    render_pestaña6()
with tab7:
    render_pestaña7()
with tab8:
    render_pestaña8()
