import streamlit as st
from ventanas.utils import enviar_a_sheets_mapeado
from config import ORDEN


# Función para convertir cadenas a mayúsculas
def to_upper(key):
    if st.session_state.get(key):
        st.session_state[key] = str(st.session_state[key]).upper()


# =====================================================
# DIÁLOGO DE CONFIRMACIÓN Y ENVÍO A GOOGLE SHEETS
# =====================================================
@st.dialog("Confirmar Captura")
def confirmar_guardado():
    st.write(
        "¿Estás seguro de que todos los datos son correctos? "
        "Al confirmar, la información se registrará en Google Sheets y el formulario se reiniciará."
    )

    if st.button("✅ Confirmar y enviar"):
        with st.spinner("Enviando datos a Google Sheets..."):
            # Llama a la función de mapeo en utils.py
            exito = enviar_a_sheets_mapeado(st.session_state.datos_completos)

        if exito:
            # Limpieza de la memoria de sesión
            st.session_state.datos_completos = {}
            st.session_state.pagina_actual = ORDEN[0]
            st.session_state.captura_exitosa = True
            st.rerun()


def render():
    st.title("Detección y Notificación de la IAAS")

    if "datos_completos" not in st.session_state:
        st.session_state.datos_completos = {}

    d = st.session_state.datos_completos.get("Deteccion", {})

    # Búsqueda segura de índices
    def buscar_idx(lista, val):
        if not val: return None
        lista_m = [str(x).lower() for x in lista]
        v_c = str(val).lower().strip()
        return lista_m.index(v_c) if v_c in lista_m else None

    # =====================================================
    # 1. PERSONAL DE NOTIFICACIÓN
    # =====================================================
    st.subheader("Personal de Notificación")

    with st.container(border=True):
        opciones_personal = [
            "MÉDICO TRATANTE",
            "MÉDICO DE LA UVEH",
            "LABORATORIO",
            "CLÍNICA DE HERIDAS",
            "HEMODIÁLISIS",
            "ENFERMERÍA",
            "ENFERMERÍA UVEH",
            "INHALOTERÁPIA",
            "CLÍNICA DE CATÉTER",
            "OTRO"
        ]

        personal_sel = st.selectbox(
            "SELECCIONE EL PERSONAL QUE NOTIFICA",
            opciones_personal,
            key="k_personal_notif",
            index=buscar_idx(opciones_personal, d.get("Personal_Notifica")),
            placeholder="Seleccione..."
        )

        espec_otro_val = ""
        if personal_sel == "OTRO":
            espec_otro_val = st.text_input(
                "Especifique otro origen:",
                key="k_esp_otro",
                value=d.get("Espec_Otro", ""),
                on_change=lambda: to_upper("k_esp_otro"),
                placeholder="Escriba el área o personal..."
            )

    # =====================================================
    # 2. RESPONSABLES
    # =====================================================
    st.subheader("Responsables")

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)

        c1.text_input(
            "RESPONSABLE DE LA DETECCIÓN",
            key="k_resp_det",
            value=d.get("Resp_Deteccion", ""),
            on_change=lambda: to_upper("k_resp_det"),
        )

        c2.text_input(
            "RESPONSABLE DE LA CAPTURA",
            key="k_resp_cap",
            value=d.get("Resp_Captura", ""),
            on_change=lambda: to_upper("k_resp_cap"),
        )

        c3.text_input(
            "RESPONSABLE DE LA UVEH",
            key="k_resp_uveh",
            value=d.get("Resp_UVEH", ""),
            on_change=lambda: to_upper("k_resp_uveh"),
        )

    # =====================================================
    # 3. UNIDAD DE DETECCIÓN
    # =====================================================
    st.subheader("Unidad de Detección")

    fue_otra_unidad = st.radio(
        "¿LA IAAS FUE ADQUIRIDA EN OTRA UNIDAD?",
        ["No", "Sí"],
        key="k_otra_unidad",
        index=buscar_idx(["No", "Sí"], d.get("Otra_Unidad", "No")),
        horizontal=True,
    )

    if fue_otra_unidad == "Sí":
        with st.container(border=True):
            st.text_input(
                "NOMBRE DE LA UNIDAD",
                key="k_nom_unidad",
                value=d.get("Nombre_Unidad", ""),
                on_change=lambda: to_upper("k_nom_unidad"),
            )

            estados = [
                "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
                "Chiapas", "Chihuahua", "CDMX", "Coahuila", "Colima", "Durango",
                "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán",
                "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro",
                "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco",
                "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
            ]

            st.selectbox(
                "ESTADO",
                estados,
                key="k_est_unidad",
                index=buscar_idx(estados, d.get("Estado_Unidad")),
                placeholder="Seleccione el estado..."
            )

    # =====================================================
    # MENSAJE DE ÉXITO TRAS REINICIO
    # =====================================================
    if st.session_state.get("captura_exitosa"):
        st.success("¡Captura registrada exitosamente en la base de datos!")
        st.session_state.captura_exitosa = False

    # =====================================================
    # FUNCIÓN INTERNA DE GUARDADO EN MEMORIA
    # =====================================================
    def guardar():
        def clean_val(val):
            return str(val).upper().strip() if val else ""

        is_otra = st.session_state.get("k_otra_unidad", "No") == "Sí"

        st.session_state.datos_completos["Deteccion"] = {
            "Personal_Notifica": clean_val(st.session_state.get("k_personal_notif")),
            "Espec_Otro": clean_val(st.session_state.get("k_esp_otro")) if st.session_state.get("k_personal_notif") == "OTRO" else "",
            "Resp_Deteccion": clean_val(st.session_state.get("k_resp_det")),
            "Resp_Captura": clean_val(st.session_state.get("k_resp_cap")),
            "Resp_UVEH": clean_val(st.session_state.get("k_resp_uveh")),
            "Otra_Unidad": clean_val(st.session_state.get("k_otra_unidad")),
            "Nombre_Unidad": clean_val(st.session_state.get("k_nom_unidad")) if is_otra else "",
            "Estado_Unidad": clean_val(st.session_state.get("k_est_unidad")) if is_otra else "",
        }

    # =====================================================
    # BOTONES DE NAVEGACIÓN Y DISPARADOR DE DIÁLOGO
    # =====================================================
    st.divider()
    c1, c2 = st.columns([1, 4])

    if c1.button("⬅️ Atrás"):
        guardar()
        st.session_state.pagina_actual = ORDEN[
            ORDEN.index(st.session_state.pagina_actual) - 1
        ]
        st.rerun()

    if c2.button("💾 Guardar y Finalizar Captura"):
        # Validación opcional de campos obligatorios
        if not st.session_state.get("k_resp_det") or not st.session_state.get("k_resp_cap"):
            st.error("Por favor complete los campos de Responsable de Detección y Captura.")
        else:
            guardar()            # 1. Guarda los datos locales
            confirmar_guardado() # 2. Dispara la ventana modal de confirmación

if __name__ == "__main__":
    render()
