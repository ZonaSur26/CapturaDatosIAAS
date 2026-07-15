import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Mi Aplicación", layout="wide")

# Inicialización de estado para la navegación
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Unidad Notificante"

def render_unidad_notificante():
    st.title("Unidad Notificante")
    st.write("Bienvenido a la sección de configuración de la Unidad Notificante.")
    
    # Aquí irán tus formularios y lógica con pandas, plotly, etc.
    with st.form("form_unidad"):
        nombre = st.text_input("Nombre de la Unidad")
        codigo = st.text_input("Código de Identificación")
        submit = st.form_submit_button("Guardar")
        
        if submit:
            st.success(f"Datos de {nombre} guardados correctamente.")

# Lógica de navegación
def main():
    st.sidebar.title("Navegación")
    
    # Menú lateral para cambiar de ventanas
    opcion = st.sidebar.radio("Ir a:", ["Unidad Notificante", "Otra Ventana"])
    
    if opcion == "Unidad Notificante":
        render_unidad_notificante()
    elif opcion == "Otra Ventana":
        st.title("Otra Ventana")
        st.write("Contenido de la siguiente sección...")

if __name__ == "__main__":
    main()
