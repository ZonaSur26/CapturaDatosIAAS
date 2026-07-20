import streamlit as st

def render():
    st.title("Tratamiento de IAAS")
    
    st.subheader("Esquema Antimicrobiano")
    
    tipo_tratamiento = st.radio("TIPO DE TRATAMIENTO", ["EMPÍRICO", "DIRIGIDO"], index=None, horizontal=True)
    
    # --- FECHAS DE TRATAMIENTO ---
    c1, c2 = st.columns(2)
    with c1:
        fecha_inicio = st.date_input("FECHA DE INICIO DE TRATAMIENTO")
    with c2:
        fecha_termino = st.date_input("FECHA DE TÉRMINO DE TRATAMIENTO", value=None)

    # --- LISTA DE ANTIMICROBIANOS ---
    # He incluido una lista representativa, puedes ampliarla según tu formulario de microbiología
    lista_ab = ["AMIKACINA", "AMPICILINA", "AZTREONAM", "CEFEPIME", "CEFTAZIDIMA", 
                "CEFTRIAXONA", "CIPROFLOXACINO", "CLINDAMICINA", "COLISTINA", 
                "DAPTOMICINA", "ERITROMICINA", "GENTAMICINA", "IMIPENEM", 
                "LEVOFLOXACINO", "LINEZOLID", "MEROPENEM", "METRONIDAZOL", 
                "PIPERACILINA-TAZOBACTAM", "TIGECICLINA", "VANCOMICINA"]
    
    antimicrobianos_selec = st.multiselect("SELECCIONE ANTIMICROBIANOS UTILIZADOS", lista_ab)
    
    if antimicrobianos_selec:
        st.write("---")
        st.markdown("### Detalles de Administración")
        for ab in antimicrobianos_selec:
            col_a, col_b, col_c = st.columns(3)
            col_a.text(f"**{ab}**")
            col_b.number_input(f"Dosis (mg/g) - {ab}", key=f"dosis_{ab}")
            col_c.selectbox(f"Frecuencia - {ab}", ["Cada 6h", "Cada 8h", "Cada 12h", "Cada 24h", "Dosis única"], key=f"freq_{ab}")

    # --- RESPUESTA CLÍNICA ---
    st.write("---")
    respuesta = st.selectbox("RESPUESTA AL TRATAMIENTO", ["MEJORÍA CLÍNICA", "SIN CAMBIOS", "EMPEORAMIENTO", "SUSPENSIÓN POR EFECTOS ADVERSOS", "ÓBITO"], index=None)
    
    if st.button("Guardar Tratamiento de IAAS"):
        st.success("Datos de tratamiento guardados exitosamente.")

if __name__ == "__main__":
    render()
