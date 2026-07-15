import streamlit as st
# Importamos las funciones desde la carpeta 'ventanas'
from ventanas.ventana1 import render_ventana1
from ventanas.ventana2 import render_ventana2
from ventanas.ventana3 import render_ventana3
from ventanas.ventana4 import render_ventana4
from ventanas.ventana5 import render_ventana5
from ventanas.ventana6 import render_ventana6
from ventanas.ventana7 import render_ventana7
from ventanas.ventana8 import render_ventana8

st.set_page_config(page_title="Sistema de Vigilancia IAAS", layout="wide")

st.title("Captura de Datos Epidemiológicos")

# Definición de las 8 pestañas (Ventanas)
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

# Renderizado de cada ventana
with tab1:
    render_ventana1()
with tab2:
    render_ventana2()
with tab3:
    render_ventana3()
with tab4:
    render_ventana4()
with tab5:
    render_ventana5()
with tab6:
    render_ventana6()
with tab7:
    render_ventana7()
with tab8:
    render_ventana8()
