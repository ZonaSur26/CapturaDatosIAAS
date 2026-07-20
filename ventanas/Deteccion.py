import streamlit as st

def render():
    st.title("Detección y Notificación de la IAAS")

    # --- APARTADO 1: ¿QUIÉN DETECTÓ LA IAAS? ---
    st.subheader("Fuente de Notificación")
    with st.container(border=True):
        # Creamos una grilla de 3 columnas para los checkboxes
        cols = st.columns(3)
        opciones = [
            "MÉDICO TRATANTE", "MÉDICO DE LA UVEH", "LABORATORIO", 
            "CLÍNICA DE HERIDAS", "HEMODIÁLISIS", "ENFERMERÍA", 
            "ENFERMERÍA UVEH", "INHALOTERÁPIA", "CLÍNICA DE CATETER"
        ]
        
        seleccionados = {}
        for i, op in enumerate(opciones):
            seleccionados[op] = cols[i % 3].checkbox(op)
        
        # Campo OTRO
        otro = st.checkbox("OTRO")
        if otro:
            st.text_input("Especifique otro origen:")

    # --- APARTADO 2: RESPONSABLES ---
    st.subheader("Responsables")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1: st.text_input("RESPONSABLE DE LA DETECCIÓN")
        with c2: st.text_input("RESPONSABLE DE LA CAPTURA")
        with c3: st.text_input("RESPONSABLE DE LA UVEH")

    # --- APARTADO 3: UNIDAD DE DETECCIÓN ---
    st.subheader("Unidad de Detección")
    fue_otra_unidad = st.radio("¿LA IAAS FUE ADQUIRIDA EN OTRA UNIDAD DE ATENCIÓN?", ["No", "Sí"], index=None, horizontal=True)

    if fue_otra_unidad == "Sí":
        with st.container(border=True):
            st.text_input("NOMBRE DE LA UNIDAD DE DONDE PROVIENE LA IAAS")
            estados = sorted([
                "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", 
                "Chihuahua", "Ciudad de México", "Coahuila", "Colima", "Durango", "Estado de México", 
                "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Michoacán", "Morelos", "Nayarit", 
                "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
                "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
            ])
            st.selectbox("ESTADO DE DONDE PROVIENE LA IAAS", estados, index=None, placeholder="Seleccione estado...")

    if st.button("Guardar Detección"):
        st.success("Datos de detección guardados.")

if __name__ == "__main__":
    render()
