import streamlit as st
import sys
import os

# Asegurar que el directorio actual esté en el path de búsqueda
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ventanas.ventana1 import render_ventana1

st.set_page_config(page_title="Sistema IAAS", layout="wide")
st.title("Captura de Datos Epidemiológicos")

# Aquí cargamos solo la ventana 1
render_ventana1()
