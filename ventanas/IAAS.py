import streamlit as st
from config import ORDEN


# =====================================================
# VENTANAS EMERGENTES (MODALES) PARA CONSULTA DE GUÍAS
# =====================================================
@st.dialog("Clasificación de Altemeier", width="large")
def mostrar_modal_altemeier():
    file_id = "1E_6Hi4lprA2I6ZsbG--fjx4UdSB4zgFU"
    url_imagen_directa = f"https://lh3.googleusercontent.com/d/{file_id}"
    st.image(url_imagen_directa, use_container_width=True)


@st.dialog("Factores de Riesgo No Contabilizables", width="large")
def mostrar_modal_no_contabilizables():
    file_id = "1KDhRlS8a37p64tiTIOTvfqaXgLXbDpvx"
    url_imagen_directa = f"https://lh3.googleusercontent.com/d/{file_id}"
    st.image(url_imagen_directa, use_container_width=True)


@st.dialog("Factores de Riesgo Contabilizables", width="large")
def mostrar_modal_contabilizables():
    file_id = "1w8T0TGKtEDJf9V0Zxjdg7i489Hf9xM7X"
    url_imagen_directa = f"https://lh3.googleusercontent.com/d/{file_id}"
    st.image(url_imagen_directa, use_container_width=True)


def render():
    st.title("IAAS y Factores de Riesgo")

    # --- CONTROL Y RECUPERACIÓN DE DATOS ---
    if "datos_completos" not in st.session_state:
        st.session_state.datos_completos = {}

    g = st.session_state.datos_completos.get("IAAS", {})

    # Listas de catálogos
    lista_iaas = [
        "CONJUNTIVITIS",
        "EMPIEMA SECUNDARIO A PROCEDIMIENTO",
        "ENDOCARDITIS",
        "ENDOFTALMITIS",
        "ENDOMETRITIS",
        "ENFERMEDAD DE LYME",
        "ERISIPELA",
        "ERITEMA INFECCIOSO",
        "EXANTEMA SECUNDARIA A MONONUCLEOSIS INFECCIOSA",
        (
            "FASCITIS NECROSANTE, GANGRENA INFECCIOSA, CELULITIS, MIOSITIS Y"
            " LINFADENITIS"
        ),
        "FLEBITIS",
        "GASTROENTERITIS",
        "INFECCIÓN DE ÓRGANOS Y ESPACIOS",
        "INFECCIÓN DE VÍAS URINARIAS ASOCIADA A CATÉTER URINARIO IVU-CU",
        "INFECCIÓN DE VÍAS URINARIAS NO ASOCIADA A CATÉTER URINARIO",
        "INFECCIÓN EN PIEL Y TEJIDOS BLANDOS",
        "INFECCIÓN EN PIEL Y TEJIDOS BLANDOS EN PACIENTES CON QUEMADURAS",
        "INFECCIÓN INCISIONAL PROFUNDA",
        "INFECCIÓN INCISIONAL SUPERFICIAL",
        "INFECCIÓN INTRACRANEAL",
        (
            "INFECCIÓN PERIPROTÉSICA (POSARTROPLASTÍA DE CADERA O"
            " RODILLA)"
        ),
        "INFECCIÓN POR CLOSTRIDIODES DIFICILE (ICD)",
        "INFECCIONES DE LA BURSA O ARTICULARES",
        (
            "INFECCIONES DEL SITIO DE INSERCIÓN DEL CATÉTER, TÚNEL O PUERTO"
            " SUBCUTÁNEO"
        ),
        "INFECCIONES RELACIONADAS A PROCEDIMIENTOS ENDOSCÓPICOS",
        "INFECCIONES RELACIONADAS A PROCEDIMIENTOS ODONTOLÓGICOS",
        "ITS RELACIONADA A CATÉTER CENTRAL (ITS - CC)",
        (
            "ITS RELACIONADA A POSIBLE CONTAMINACIÓN DE SOLUCIONES, INFUSIONES O"
            " MEDICAMENTOS"
        ),
        "ITS RELACIONADA A PROCEDIMIENTO (ITS-RP)",
        "ITS SECUNDARIO A DAÑO DE LA BARRERA MICOSA (ITS - DBM)",
        "MEDIASTINITIS",
        "MENINGITIS O VENTRICULITIS SECUNDARIA A UN PROCEDIMIENTO DEL SNC",
        "MIOCARDITIS",
        "NAAS NO RELACIONADA A PROCEDIMIENTO (NAAS - NRP)",
        "NAAS RELACIONADA A PROCEDIMIENTO (NAAS - RP)",
        "NEUMONÍA ASOCIADA A VENTILADOR (NAV)",
        "OSTEOMIELITIS",
        "OTITIS MEDIA AGUDA",
        "OTRO",
        "PERICARDITIS",
        "PERITONITIS ASOCIADA A DIÁLISIS",
        (
            "PERITONITIS ASOCIADA A LA INSTALACIÓN DE CATÉTER DE DIÁLISIS"
            " PERITONEAL"
        ),
        "RINOFARINGITIS Y FARINGOAMIGDALITIS",
        "RUBÉOLA",
        "SARAMPIÓN",
        "SINDROME DE CHOQUE TÓXICO",
        "SINDROME DE PIEL ESCALDADA",
        "SINDROME PIE-MANO-BOCA",
        "SINUSITIS AGUDA",
        "STAPHYLOCOCCEMIA",
        "VARICELA",
    ]

    opciones_det = ["Definida clinicamente", "Confirmada por laboratorio"]
    opciones_nc = [
        "AMNIOCENTESIS",
        "ANGIOPLASTIA",
        "ASPIRADO DE MEDULA OSEA",
        "BRONCOASPIRACIÓN SECUNDARIA A UN PROCEDIMIENTO",
        "BRONCOSCOPIA Y/O LAVADO BRONQUIAL",
        "CATETERISMO CARDIOVASCULAR",
        "CATETERISMO RIGIDO",
        "CATETERISMO VESICAL DE ENTRADA POR SALIDA",
        "COLONOSCOPIA",
        "DEPRESIÓN DEL ESTADO DE CONCIENCIA",
        "ESCALAMIENTO ANTIMICROBIANO SIN JUSTIFICACIÓN",
        "LAPAROSCOPIA",
        "LARINGOSCOPIA",
        "MARCAPASO DEFINITIVO",
        "NEFROSTOMIA",
        "PANENDOSCOPIA",
        "PARACENTESIS-TORACOCENTESIS",
        "PLASMAFERESIS/OTRAS AFERESIS",
        "PROFILAXIS ANTIMICROBIANA INADECUADA",
        "PUNCIÓN LUMBAR",
        "PUNCIÓN PLEURAL",
        "REINSTALACIÓN DE OTRO DISPOSITIVO INVASIVO",
        "REINSTALACIÓN DE CATÉTER VENOSO CENTRAL",
        "REINSTALACIÓN DE CATÉTER URINARIO",
        "REINSTALACIÓN DE CÁNULA OROTRAQUEAL",
        "RUPTURA PREMATURA DE MEMBRANAS",
        "TIEMPO DE CIRUGÍA PROLONGADO",
        "TRANSFUSIÓN",
        "TRASPLANTE",
    ]
    opciones_c = [
        "ALIMENTACIÓN ENTERAL A TRAVÉS DE SONDA",
        "DISPOSITIVO SUBCUTÁNEO",
        "ANTIBIÓTICOS PREVIOS (3 SEMANAS PREVIAS A LA IAAS)",
        "DRENAJE QUIRÚRGICO",
        (
            "ANTIBIÓTICOS DE AMPLIO ESPECTRO (HASTA 3 SEMANAS PREVIAS A LA"
            " IAAS)"
        ),
        "ESTANCIA EN UNIDAD DE TERAPIA INTENSIVA",
        "USO MÚLTIPLE DE ESQUEMA ANTIMICROBIANO (SIMULTANEO)",
        "ESTANCIA EN URGENCIAS",
        (
            "USO DE ANTIÁCIDOS (INHIBIDORES DE BOMBA DE PROTONES O INHIBIDORES"
            " H2)"
        ),
        "ESTANCIA PROLONGADA",
        "BALÓN INTRAORTICO (BIAC)",
        "NEUTROPENIA (MENOS DE 500 NEUTRÓFILOS TOTALES)",
        "BOMBA DE CIRCULACIÓN EXTRACORPOREAL",
        "NUTRICIÓN PARENTERAL",
        "CASCO CEFÁLICO",
        "QUIMIOTERAPIA (3 SEMANAS PREVIAS A LA IAAS)",
        "CATÉTER VENOSO CENTRAL",
        "RADIOTERAPIA (4 SEMANAS PREVIAS A LA IAAS)",
        "CATÉTER DE URETEROSTOMIA",
        "RESERVORIO DE OMMAYA",
        "CATÉTER EPIDURAL",
        "RETENCIÓN DE RESTOS PLACENTARIOS",
        "CATÉTER FLOTACIÓN PULMONAR (SWAN GANZ)",
        "SONDA DE BALONES (SENGSTAKEN-BLAKEMORE)",
        "CATÉTER HEMODIÁLISIS",
        "SONDA DE CORTA PERMANENCIA",
        "CATÉTER TENCHKOFF",
        "SONDA DE GASTROSTOMÍA",
        "CATETERISMO UMBILICAL",
        "SONDA DE YEYUNOSTOMÍA",
        "DERIVACIÓN URINARIA CONTINENTE",
        "SONDA MEDIASTINAL",
        "DERIVACIÓN BILIAR",
        "SONDA NASOGÁSTRICA",
        "DERIVACIÓN VENTRICULAR ABIERTA",
        "SONDA OROGÁSTRICA",
        "DERIVACIÓN VENTRICULAR CERRADA",
        "SONDA PLEURAL",
        "DIÁLISIS PERITONEAL",
        "CATÉTER URINARIO",
    ]

    def buscar_idx(lista, val):
        if not val:
            return None
        lista_m = [str(x).lower() for x in lista]
        v_c = str(val).lower().strip()
        return lista_m.index(v_c) if v_c in lista_m else None

    with st.container(border=True):
        # --- 2. CLASIFICACIÓN ---
        st.subheader("Clasificación de la IAAS")
        c1, c2 = st.columns(2)

        with c1:
            tipo_iaas = st.selectbox(
                "Tipo de IAAS",
                lista_iaas,
                key="k_tipo",
                index=buscar_idx(lista_iaas, g.get("Tipo")),
                placeholder="Seleccione...",
            )

            # Reactividad libre de campo condicional OTRO
            if tipo_iaas == "OTRO":
                st.text_input(
                    "Especifique la IAAS:", key="k_otro", value=g.get("Otro", "")
                )

            tipo_deteccion = st.selectbox(
                "Tipo de detección",
                opciones_det,
                key="k_tipo_det",
                index=buscar_idx(opciones_det, g.get("tipo_deteccion")),
                placeholder="Seleccione...",
            )

        with c2:
            brote = st.radio(
                "¿El caso forma parte de un brote?",
                ["No", "Sí"],
                key="k_brote",
                index=buscar_idx(["No", "Sí"], g.get("Brote", "No")),
                horizontal=True,
            )
            if brote == "Sí":
                st.text_input(
                    "Folio NOTINMED", key="k_folio", value=g.get("Folio", "")
                )

    # --- CIRUGÍAS ---
    st.subheader("Cirugías relacionadas con la IAAS (Máximo 4)")

    # BOTÓN CONSULTA ALTEMEIER
    if st.button(
        "👁️ Consultar Grados de Contaminación (Clasificación de Altemeier)",
        key="k_btn_altemeier",
        type="primary",
        use_container_width=True,
    ):
        mostrar_modal_altemeier()

    st.write("")

    for i in range(1, 5):
        with st.expander(f"Captura de Cirugía {i}"):
            cols = st.columns(3)
            with cols[0]:
                st.date_input(
                    f"Fecha de cirugía {i}",
                    key=f"f_cir_{i}",
                    value=g.get(f"f_cir_{i}", None),
                    format="DD/MM/YYYY",
                )
                st.selectbox(
                    f"Tipo {i}",
                    ["Electiva", "Urgencia"],
                    key=f"tipo_cir_{i}",
                    index=buscar_idx(
                        ["Electiva", "Urgencia"], g.get(f"tipo_cir_{i}")
                    ),
                    placeholder="Seleccione...",
                )
            with cols[1]:
                grados = [
                    "Limpia",
                    "Limpia con implante",
                    "Limpia contaminada",
                    "Contaminada",
                    "Sucia",
                ]
                st.selectbox(
                    f"Grado de contaminación {i}",
                    grados,
                    key=f"grado_{i}",
                    index=buscar_idx(grados, g.get(f"grado_{i}")),
                    placeholder="Seleccione...",
                )
                st.radio(
                    f"¿Se colocó prótesis? {i}",
                    ["No", "Sí"],
                    horizontal=True,
                    key=f"protesis_{i}",
                    index=buscar_idx(
                        ["No", "Sí"], g.get(f"protesis_{i}")
                    ),
                )
            with cols[2]:
                st.text_input(
                    f"Procedimiento quirúrgico {i}",
                    key=f"proc_{i}",
                    value=g.get(f"proc_{i}", ""),
                    placeholder="Ej. Apendicectomía...",
                )

    # --- FACTORES DE RIESGO NO CONTABILIZABLES ---
    st.subheader("Factores de riesgo no contabilizables")

    # BOTÓN CONSULTA NO CONTABILIZABLES
    if st.button(
        "👁️ Consultar Factores de Riesgo No Contabilizables",
        key="k_btn_no_contabilizables",
        type="primary",
        use_container_width=True,
    ):
        mostrar_modal_no_contabilizables()

    st.write("")

    for i in range(1, 6):
        c1, c2 = st.columns([2, 1])
        c1.selectbox(
            f"Factores de riesgo no contabilizable {i}",
            opciones_nc,
            key=f"nc_{i}",
            index=buscar_idx(opciones_nc, g.get(f"nc_{i}")),
            placeholder="Seleccione...",
        )
        c2.date_input(
            f"Fecha de ocurrencia {i}",
            key=f"f_nc_{i}",
            value=g.get(f"f_nc_{i}", None),
            format="DD/MM/YYYY",
        )

    # --- FACTORES DE RIESGO CONTABILIZABLES ---
    st.subheader("Factores de riesgo contabilizables")

    # BOTÓN CONSULTA CONTABILIZABLES
    if st.button(
        "👁️ Consultar Factores de Riesgo Contabilizables",
        key="k_btn_contabilizables",
        type="primary",
        use_container_width=True,
    ):
        mostrar_modal_contabilizables()

    st.write("")

    for i in range(1, 6):
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.selectbox(
            f"Factores de riesgo contabilizable {i}",
            opciones_c,
            key=f"c_{i}",
            index=buscar_idx(opciones_c, g.get(f"c_{i}")),
            placeholder="Seleccione...",
        )
        c2.date_input(
            f"Fecha de instalación {i}",
            key=f"f_inst_{i}",
            value=g.get(f"f_inst_{i}", None),
            format="DD/MM/YYYY",
        )
        c3.date_input(
            f"Fecha de retiro {i}",
            key=f"f_ret_{i}",
            value=g.get(f"f_ret_{i}", None),
            format="DD/MM/YYYY",
        )

    # --- LÓGICA DE GUARDADO COMPLETA ---
    def guardar():
        def clean_txt(key):
            val = st.session_state.get(key, "")
            return str(val).upper().strip() if val else ""

        def clean_val(val):
            return str(val).upper().strip() if val else ""

        # Inicializamos el diccionario base
        datos_iaas = {
            "Tipo": clean_val(tipo_iaas),
            "tipo_deteccion": clean_val(tipo_deteccion),
            "Brote": clean_val(brote),
            "Otro": clean_txt("k_otro") if tipo_iaas == "OTRO" else "",
            "Folio": clean_txt("k_folio") if brote == "Sí" else "",
        }

        # Guardado dinámico del bloque de Cirugías (1 a 4)
        for i in range(1, 5):
            datos_iaas[f"f_cir_{i}"] = st.session_state.get(f"f_cir_{i}")
            datos_iaas[f"tipo_cir_{i}"] = clean_val(
                st.session_state.get(f"tipo_cir_{i}")
            )
            datos_iaas[f"grado_{i}"] = clean_val(
                st.session_state.get(f"grado_{i}")
            )
            datos_iaas[f"protesis_{i}"] = clean_val(
                st.session_state.get(f"protesis_{i}")
            )
            datos_iaas[f"proc_{i}"] = clean_txt(f"proc_{i}")

        # Guardado dinámico de Riesgos No Contabilizables (1 a 5)
        for i in range(1, 6):
            datos_iaas[f"nc_{i}"] = clean_val(st.session_state.get(f"nc_{i}"))
            datos_iaas[f"f_nc_{i}"] = st.session_state.get(f"f_nc_{i}")

        # Guardado dinámico de Riesgos Contabilizables (1 a 5)
        for i in range(1, 6):
            datos_iaas[f"c_{i}"] = clean_val(st.session_state.get(f"c_{i}"))
            datos_iaas[f"f_inst_{i}"] = st.session_state.get(f"f_inst_{i}")
            datos_iaas[f"f_ret_{i}"] = st.session_state.get(f"f_ret_{i}")

        # Asignación final al session_state global
        st.session_state.datos_completos["IAAS"] = datos_iaas
        st.session_state.habilitar_microbiologia = (
            tipo_deteccion == "Confirmada por laboratorio"
        )

    # --- NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])

    if col_atras.button("⬅️ Atrás"):
        guardar()
        st.session_state.pagina_actual = ORDEN[
            ORDEN.index(st.session_state.pagina_actual) - 1
        ]
        st.rerun()

    if col_guardar.button("💾 Guardar registro y continuar"):
        if not tipo_iaas or not tipo_deteccion:
            st.error(
                "Por favor, selecciona los campos obligatorios (Tipo de IAAS y"
                " Tipo de detección)."
            )
        else:
            guardar()
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[idx + 1]
                st.rerun()


if __name__ == "__main__":
    render()
