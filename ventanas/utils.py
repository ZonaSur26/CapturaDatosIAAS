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
@st.dialog("Confirmar Envío de Datos")
def confirmar_guardado():
    st.write(
        "¿Estás seguro de que todos los datos registrados son correctos? "
        "Al confirmar, la información se guardará en Google Sheets."
    )

    if st.button("✅ Confirmar y Enviar", use_container_width=True):
        with st.spinner("Guardando registro en la base de datos..."):
            exito = enviar_a_sheets_mapeado(st.session_state.datos_completos)

        if exito:
            # Marcamos el éxito y guardamos un resumen básico para mostrarlo en pantalla
            st.session_state.captura_exitosa = True
            st.session_state.resumen_paciente = {
                "expediente": st.session_state.datos_completos.get("Paciente", {}).get("Expediente", "N/A"),
                "nombre": f"{st.session_state.datos_completos.get('Paciente', {}).get('Nombres', '')} {st.session_state.datos_completos.get('Paciente', {}).get('Ap_Paterno', '')}".strip() or "N/A",
                "mes": st.session_state.datos_completos.get("Unidad", {}).get("Mes", "Actual")
            }
            st.rerun()


def render():
    st.title("Detección y Notificación de la IAAS")

    if "datos_completos" not in st.session_state:
        st.session_state.datos_completos = {}

    # Búsqueda segura de índices
    def buscar_idx(lista, val):
        if not val: return None
        lista_m = [str(x).lower() for x in lista]
        v_c = str(val).lower().strip()
        return lista_m.index(v_c) if v_c in lista_m else None

    # =====================================================
    # PANACEA DE ÉXITO: SI YA SE GUARDARON LOS DATOS
    # =====================================================
    if st.session_state.get("captura_exitosa"):
        resumen = st.session_state.get("resumen_paciente", {})
        
        st.balloons() # Animación amigable de éxito
        
        st.success("🎉 ¡Los datos se han guardado correctamente en Google Sheets!")
        
        with st.container(border=True):
            st.markdown("### 📋 Resumen del Registro Exitoso")
            st.markdown(f"**Paciente:** {resumen.get('nombre', 'N/A')}")
            st.markdown(f"**Expediente:** {resumen.get('expediente', 'N/A')}")
            st.markdown(f"**Pestaña / Mes de Registro:** {resumen.get('mes', 'N/A')}")
            st.info("El formulario se encuentra listo para iniciar la captura de un nuevo paciente.")

        if st.button("➕ Iniciar Nueva Captura", type="primary", use_container_width=True):
            # Limpiamos la sesión y reiniciamos a la Ventana 1
            st.session_state.datos_completos = {}
            st.session_state.captura_exitosa = False
            st.session_state.resumen_paciente = None
            st.session_state.pagina_actual = ORDEN[0]
            st.rerun()
            
        return  # Detiene la renderización del formulario mientras se muestra la pantalla de éxito

    # =====================================================
    # DILIGENCIAMIENTO NORMAL DE LA VENTANA 9
    # =====================================================
    d = st.session_state.datos_completos.get("Deteccion", {})

    st.subheader("Personal de Notificación")
    with st.container(border=True):
        opciones_personal = [
            "MÉDICO TRATANTE", "MÉDICO DE LA UVEH", "LABORATORIO", "CLÍNICA DE HERIDAS",
            "HEMODIÁLISIS", "ENFERMERÍA", "ENFERMERÍA UVEH", "INHALOTERÁPIA",
            "CLÍNICA DE CATÉTER", "OTRO"
        ]

        personal_sel = st.selectbox(
            "SELECCIONE EL PERSONAL QUE NOTIFICA",
            opciones_personal,
            key="k_personal_notif",
            index=buscar_idx(opciones_personal, d.get("Personal_Notifica")),
            placeholder="Seleccione..."
        )

        if personal_sel == "OTRO":
            st.text_input(
                "Especifique otro origen:",
                key="k_esp_otro",
                value=d.get("Espec_Otro", ""),
                on_change=lambda: to_upper("k_esp_otro"),
                placeholder="Escriba el área o personal..."
            )

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
    # NAVEGACIÓN
    # =====================================================
    st.divider()
    c1, c2 = st.columns([1, 4])

    if c1.button("⬅️ Atrás"):
        guardar()
        st.session_state.pagina_actual = ORDEN[
            ORDEN.index(st.session_state.pagina_actual) - 1
        ]
        st.rerun()

    if c2.button("💾 Guardar y Finalizar Captura", type="primary"):
        if not st.session_state.get("k_resp_det") or not st.session_state.get("k_resp_cap"):
            st.error("⚠️ Por favor complete los campos de Responsable de Detección y Captura.")
        else:
            guardar()
            confirmar_guardado()


if __name__ == "__main__":
    render()
