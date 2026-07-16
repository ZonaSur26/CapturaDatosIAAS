# --- CIRUGÍAS ---
    st.subheader("Cirugías relacionadas con la IAAS (Máximo 4)")
    for i in range(1, 5):
        with st.expander(f"Captura de Cirugía {i}"):
            cols = st.columns(3)
            with cols[0]:
                st.date_input(f"Fecha de cirugía {i}", key=f"f_cir_{i}", value=None)
                st.selectbox(
                    f"Tipo {i}", 
                    ["Electiva", "Urgencia"], 
                    key=f"tipo_cir_{i}", 
                    index=None, 
                    placeholder="Seleccione..."
                )
            with cols[1]:
                st.selectbox(
                    f"Grado de contaminación {i}", 
                    ["Limpia", "Limpia con implante", "Limpia contaminada", "Contaminada", "Sucia"], 
                    key=f"grado_{i}", 
                    index=None, 
                    placeholder="Seleccione..."
                )
                st.radio(
                    f"¿Se colocó prótesis? {i}", 
                    ["No", "Sí"], 
                    horizontal=True, 
                    key=f"protesis_{i}", 
                    index=None # Esto asegura que no haya selección inicial
                )
            with cols[2]:
                st.text_input(f"Procedimiento quirúrgico {i}", key=f"proc_{i}", placeholder="Ej. Apendicectomía...")
