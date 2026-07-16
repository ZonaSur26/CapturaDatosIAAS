import streamlit as st

def render():
    st.title("IAAS y Factores de Riesgo")

    # --- CLASIFICACIÓN ---
    st.subheader("Clasificación de la IAAS")
    c1, c2 = st.columns(2)
    with c1:
        tipo_iaas = st.selectbox("Tipo de IAAS", ["Infección del Torrente Sanguíneo", "ITU", "Neumonía", "Sitio Quirúrgico", "Otras"], index=None)
        tipo_deteccion = st.selectbox("Tipo de detección", ["Definida clinicamente", "Confirmada por laboratorio"], index=None)
    
    brote = st.radio("¿El caso forma parte de un brote?", ["No", "Sí"], horizontal=True)
    folio_notinmed = st.text_input("Folio NOTINMED") if brote == "Sí" else None

    # --- CIRUGÍAS RELACIONADAS ---
    st.subheader("Cirugías relacionadas con la IAAS (Máximo 4)")
    for i in range(1, 5):
        with st.expander(f"Captura de Cirugía {i}"):
            cols = st.columns(3)
            with cols[0]:
                st.date_input(f"Fecha de cirugía {i}", key=f"f_cir_{i}")
                st.selectbox(f"Tipo {i}", ["Electiva", "Urgencia"], key=f"tipo_cir_{i}")
            with cols[1]:
                st.selectbox(f"Grado de contaminación {i}", ["Limpia", "Limpia con implante", "Limpia contaminada", "Contaminada", "Sucia"], key=f"grado_{i}")
                st.radio(f"¿Se colocó prótesis? {i}", ["No", "Sí"], horizontal=True, key=f"protesis_{i}")
            with cols[2]:
                st.text_input(f"Procedimiento quirúrgico {i}", key=f"proc_{i}")

    # --- LISTAS DE REFERENCIA ---
    opciones_no_contabilizables = [
        "AMNIOCENTESIS", "ANGIOPLASTIA", "ASPIRADO DE MEDULA OSEA", "BRONCOASPIRACIÓN SECUNDARIA A UN PROCEDIMIENTO",
        "BRONCOSCOPIA Y/O LAVADO BRONQUIAL", "CATETERISMO CARDIOVASCULAR", "CATETERISMO RIGIDO", "CATETERISMO VESICAL DE ENTRADA POR SALIDA",
        "COLONOSCOPIA", "DEPRESIÓN DEL ESTADO DE CONCIENCIA", "ESCALAMIENTO ANTIMICROBIANO SIN JUSTIFICACIÓN",
        "LAPAROSCOPIA", "LARINGOSCOPIA", "MARCAPASO DEFINITIVO", "NEFROSTOMIA", "PANENDOSCOPIA", "PARACENTESIS-TORACOCENTESIS",
        "PLASMAFERESIS/OTRAS AFERESIS", "PROFILAXIS ANTIMICROBIANA INADECUADA", "PUNCIÓN LUMBAR", "PUNCIÓN PLEURAL",
        "REINSTALACIÓN DE OTRO DISPOSITIVO INVASIVO", "REINSTALACIÓN DE CATÉTER VENOSO CENTRAL", "REINSTALACIÓN DE CATÉTER URINARIO",
        "REINSTALACIÓN DE CÁNULA OROTRAQUEAL", "RUPTURA PREMATURA DE MEMBRANAS", "TIEMPO DE CIRUGÍA PROLONGADO", "TRANSFUSIÓN", "TRASPLANTE"
    ]

    opciones_contabilizables = [
        "ALIMENTACIÓN ENTERAL", "ANTIBIÓTICOS PREVIOS", "ANTIBIÓTICOS DE AMPLIO ESPECTRO", "BALÓN INTRAORTICO", 
        "BOMBA DE CIRCULACIÓN EXTRACORPOREAL", "CATÉTER VENOSO CENTRAL", "CATÉTER URINARIO", "DIÁLISIS PERITONEAL",
        "ESTANCIA EN TERAPIA INTENSIVA", "NUTRICIÓN PARENTERAL", "QUIMIOTERAPIA", "RADIOTERAPIA", "SONDA NASOGÁSTRICA"
    ]

    # --- FACTORES NO CONTABILIZABLES ---
    st.subheader("Factores de riesgo no contabilizables")
    for i in range(1, 6):
        c1, c2 = st.columns([2, 1])
        c1.selectbox(f"Evento {i}", opciones_no_contabilizables, key=f"nc_{i}", index=None)
        c2.date_input(f"Fecha {i}", key=f"f_nc_{i}")

    # --- FACTORES CONTABILIZABLES ---
    st.subheader("Factores de riesgo contabilizables")
    for i in range(1, 6):
        c1, c2, c3 = st.columns(3)
        c1.selectbox(f"Factor {i}", opciones_contabilizables, key=f"c_{i}", index=None)
        c2.date_input(f"Instalación {i}", key=f"f_inst_{i}")
        c3.date_input(f"Retiro {i}", key=f"f_ret_{i}")

    if st.button("Guardar IAAS"):
        st.success("Datos guardados correctamente.")
