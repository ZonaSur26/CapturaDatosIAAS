import streamlit as st

def render():
    st.title("IAAS y Factores de Riesgo")

    # --- CLASIFICACIÓN DE LA IAAS ---
    st.subheader("Clasificación de la IAAS")
    c1, c2 = st.columns(2)
    with c1:
        lista_iaas = [
            "CONJUNTIVITIS", "EMPIEMA SECUNDARIO A PROCEDIMIENTO", "ENDOCARDITIS", "ENDOFTALMITIS", 
            "ENDOMETRITIS", "ENFERMEDAD DE LYME", "ERISIPELA", "ERITEMA INFECCIOSO", 
            "EXANTEMA SECUNDARIA A MONONUCLEOSIS INFECCIOSA", 
            "FASCITIS NECROSANTE, GANGRENA INFECCIOSA, CELULITIS, MIOSITIS Y LINFADENITIS", 
            "FLEBITIS", "GASTROENTERITIS", "INFECCIÓN DE ÓRGANOS Y ESPACIOS", 
            "INFECCIÓN DE VÍAS URINARIAS ASOCIADA A CATÉTER URINARIO IVU-CU", 
            "INFECCIÓN DE VÍAS URINARIAS NO ASOCIADA A CATÉTER URINARIO", 
            "INFECCIÓN EN PIEL Y TEJIDOS BLANDOS", 
            "INFECCIÓN EN PIEL Y TEJIDOS BLANDOS EN PACIENTES CON QUEMADURAS", 
            "INFECCIÓN INCISIONAL PROFUNDA", "INFECCIÓN INCISIONAL SUPERFICIAL", 
            "INFECCIÓN INTRACRANEAL", "INFECCIÓN PERIPROTÉSICA (POSARTROPLASTÍA DE CADERA O RODILLA)", 
            "INFECCIÓN POR CLOSTRIDIODES DIFICILE (ICD)", "INFECCIONES DE LA BURSA O ARTICULARES", 
            "INFECCIONES DEL SITIO DE INSERCIÓN DEL CATÉTER, TÚNEL O PUERTO SUBCUTÁNEO", 
            "INFECCIONES RELACIONADAS A PROCEDIMIENTOS ENDOSCÓPICOS", 
            "INFECCIONES RELACIONADAS A PROCEDIMIENTOS ODONTOLÓGICOS", 
            "ITS RELACIONADA A CATÉTER CENTRAL (ITS - CC)", 
            "ITS RELACIONADA A POSIBLE CONTAMINACIÓN DE SOLUCIONES, INFUSIONES O MEDICAMENTOS", 
            "ITS RELACIONADA A PROCEDIMIENTO (ITS-RP)", 
            "ITS SECUNDARIO A DAÑO DE LA BARRERA MICOSA (ITS - DBM)", "MEDIASTINITIS", 
            "MENINGITIS O VENTRICULITIS SECUNDARIA A UN PROCEDIMIENTO DEL SNC", 
            "MIOCARDITIS", "NAAS NO RELACIONADA A PROCEDIMIENTO (NAAS - NRP)", 
            "NAAS RELACIONADA A PROCEDIMIENTO (NAAS - RP)", "NEUMONÍA ASOCIADA A VENTILADOR (NAV)", 
            "OSTEOMIELITIS", "OTITIS MEDIA AGUDA", "OTRO", "PERICARDITIS", 
            "PERITONITIS ASOCIADA A DIÁLISIS", 
            "PERITONITIS ASOCIADA A LA INSTALACIÓN DE CATÉTER DE DIÁLISIS PERITONEAL", 
            "RINOFARINGITIS Y FARINGOAMIGDALITIS", "RUBÉOLA", "SARAMPIÓN", 
            "SINDROME DE CHOQUE TÓXICO", "SINDROME DE PIEL ESCALDADA", 
            "SINDROME PIE-MANO-BOCA", "SINUSITIS AGUDA", "STAPHYLOCOCCEMIA", "VARICELA"
        ]
        tipo_iaas = st.selectbox("Tipo de IAAS", lista_iaas, index=None, placeholder="Seleccione...")
        if tipo_iaas == "OTRO":
            especificar_otra = st.text_input("Especifique la IAAS:")
            
        tipo_deteccion = st.selectbox("Tipo de detección", ["Definida clinicamente", "Confirmada por laboratorio"], index=None, placeholder="Seleccione...")
    
    brote = st.radio("¿El caso forma parte de un brote?", ["No", "Sí"], index=None, horizontal=True)
    if brote == "Sí":
        folio_notinmed = st.text_input("Folio NOTINMED")

    # --- CIRUGÍAS RELACIONADAS ---
    st.subheader("Cirugías relacionadas con la IAAS (Máximo 4)")
    for i in range(1, 5):
        with st.expander(f"Captura de Cirugía {i}"):
            cols = st.columns(3)
            with cols[0]:
                st.date_input(f"Fecha de cirugía {i}", key=f"f_cir_{i}", value=None)
                st.selectbox(f"Tipo {i}", ["Electiva", "Urgencia"], key=f"tipo_cir_{i}", index=None, placeholder="Seleccione...")
            with cols[1]:
                st.selectbox(f"Grado de contaminación {i}", ["Limpia", "Limpia con implante", "Limpia contaminada", "Contaminada", "Sucia"], key=f"grado_{i}", index=None, placeholder="Seleccione...")
                st.radio(f"¿Se colocó prótesis? {i}", ["No", "Sí"], horizontal=True, key=f"protesis_{i}", index=None)
            with cols[2]:
                st.text_input(f"Procedimiento quirúrgico {i}", key=f"proc_{i}", placeholder="Ej. Apendicectomía...")

    # --- LISTAS DE REFERENCIA ---
    opciones_nc = ["AMNIOCENTESIS", "ANGIOPLASTIA", "ASPIRADO DE MEDULA OSEA", "BRONCOASPIRACIÓN SECUNDARIA A UN PROCEDIMIENTO", "BRONCOSCOPIA Y/O LAVADO BRONQUIAL", "CATETERISMO CARDIOVASCULAR", "CATETERISMO RIGIDO", "CATETERISMO VESICAL DE ENTRADA POR SALIDA", "COLONOSCOPIA", "DEPRESIÓN DEL ESTADO DE CONCIENCIA", "ESCALAMIENTO ANTIMICROBIANO SIN JUSTIFICACIÓN", "LAPAROSCOPIA", "LARINGOSCOPIA", "MARCAPASO DEFINITIVO", "NEFROSTOMIA", "PANENDOSCOPIA", "PARACENTESIS-TORACOCENTESIS", "PLASMAFERESIS/OTRAS AFERESIS", "PROFILAXIS ANTIMICROBIANA INADECUADA", "PUNCIÓN LUMBAR", "PUNCIÓN PLEURAL", "REINSTALACIÓN DE OTRO DISPOSITIVO INVASIVO", "REINSTALACIÓN DE CATÉTER VENOSO CENTRAL", "REINSTALACIÓN DE CATÉTER URINARIO", "REINSTALACIÓN DE CÁNULA OROTRAQUEAL", "RUPTURA PREMATURA DE MEMBRANAS", "TIEMPO DE CIRUGÍA PROLONGADO", "TRANSFUSIÓN", "TRASPLANTE"]
    
    opciones_c = ["ALIMENTACIÓN ENTERAL A TRAVÉS DE SONDA", "DISPOSITIVO SUBCUTÁNEO", "ANTIBIÓTICOS PREVIOS (3 SEMANAS PREVIAS A LA IAAS)", "DRENAJE QUIRÚRGICO", "ANTIBIÓTICOS DE AMPLIO ESPECTRO (HASTA 3 SEMANAS PREVIAS A LA IAAS)", "ESTANCIA EN UNIDAD DE TERAPIA INTENSIVA", "USO MÚLTIPLE DE ESQUEMA ANTIMICROBIANO (SIMULTANEO)", "ESTANCIA EN URGENCIAS", "USO DE ANTIÁCIDOS (INHIBIDORES DE BOMBA DE PROTONES O INHIBIDORES H2)", "ESTANCIA PROLONGADA", "BALÓN INTRAORTICO (BIAC)", "NEUTROPENIA (MENOS DE 500 NEUTRÓFILOS TOTALES)", "BOMBA DE CIRCULACIÓN EXTRACORPOREAL", "NUTRICIÓN PARENTERAL", "CASCO CEFÁLICO", "QUIMIOTERAPIA (3 SEMANAS PREVIAS A LA IAAS)", "CATÉTER VENOSO CENTRAL", "RADIOTERAPIA (4 SEMANAS PREVIAS A LA IAAS)", "CATÉTER DE URETEROSTOMIA", "RESERVORIO DE OMMAYA", "CATÉTER EPIDURAL", "RETENCIÓN DE RESTOS PLACENTARIOS", "CATÉTER FLOTACIÓN PULMONAR (SWAN GANZ)", "SONDA DE BALONES (SENGSTAKEN-BLAKEMORE)", "CATÉTER HEMODIÁLISIS", "SONDA DE CORTA PERMANENCIA", "CATÉTER TENCHKOFF", "SONDA DE GASTROSTOMÍA", "CATETERISMO UMBILICAL", "SONDA DE YEYUNOSTOMÍA", "DERIVACIÓN URINARIA CONTINENTE", "SONDA MEDIASTINAL", "DERIVACIÓN BILIAR", "SONDA NASOGÁSTRICA", "DERIVACIÓN VENTRICULAR ABIERTA", "SONDA OROGÁSTRICA", "DERIVACIÓN VENTRICULAR CERRADA", "SONDA PLEURAL", "DIÁLISIS PERITONEAL", "CATÉTER URINARIO"]

    # --- FACTORES ---
    st.subheader("Factores de riesgo no contabilizables")
    for i in range(1, 6):
        c1, c2 = st.columns([2, 1])
        c1.selectbox(f"Evento {i}", opciones_nc, key=f"nc_{i}", index=None, placeholder="Seleccione...")
        c2.date_input(f"Fecha {i}", key=f"f_nc_{i}", value=None)

    st.subheader("Factores de riesgo contabilizables")
    for i in range(1, 6):
        with st.expander(f"Factor Contabilizable {i}"):
            c1, c2, c3 = st.columns(3)
            c1.selectbox(f"Factor {i}", opciones_c, key=f"c_{i}", index=None, placeholder="Seleccione...")
            c2.date_input(f"Instalación {i}", key=f"f_inst_{i}", value=None)
            c3.date_input(f"Retiro {i}", key=f"f_ret_{i}", value=None)

    if st.button("Guardar IAAS"):
        st.success("Datos de IAAS guardados correctamente.")

```
