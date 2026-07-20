import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from config import ORDEN

# Función para forzar mayúsculas en callbacks
def to_upper(key):
    st.session_state[key] = str(st.session_state[key]).upper()

def render():
    st.title("Identificación del Paciente")

    # --- RECUPERACIÓN DE DATOS GUARDADOS ---
    g = st.session_state.datos_completos.get("Paciente", {})

    # Definición de listas (omito repetir las listas para brevedad pero deben estar aquí)
    estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
    lista_esc = ["Sin estudios", "Primaria incompleta", "Primaria terminada", "Secundaria incompleta", "Secundaria terminada", "Preparatoria incompleta", "Preparatoria terminada", "Licenciatura incompleta", "Licenciatura terminada", "Posgrado", "Especialidad", "Maestría", "Doctorado", "Se desconoce"]
    lista_ocu = ["Campesino", "Chofer", "Comerciante", "Dentista", "Desempleado", "Empleado", "Enfermera", "Estudiante", "Gerente", "Hogar", "Jubilado", "Laboratorista", "Maestro", "Médico", "Otros oficios", "Otro Profesionista", "Otro trabajador de salud", "Se ignora", "No aplica"]
    paises = sorted(["Alemania", "Argentina", "Belice", "Bolivia", "Brasil", "Canadá", "Chile", "Colombia", "Costa Rica", "Cuba", "Ecuador", "El Salvador", "Estados Unidos", "Guatemala", "Haití", "Honduras", "México", "Nicaragua", "Panamá", "Paraguay", "Perú", "República Dominicana", "Uruguay", "Venezuela"])

    # --- DATOS GENERALES ---
    st.subheader("Datos Generales")
    st.text_input("Nº de expediente", key="Expediente", value=g.get("Expediente", ""), placeholder="Ej. 123456", on_change=to_upper, args=["Expediente"])
    
    c1, c2, c3 = st.columns(3)
    c1.text_input("Apellido Paterno", key="Ap_Paterno", value=g.get("Ap_Paterno", ""), on_change=to_upper, args=["Ap_Paterno"])
    c2.text_input("Apellido Materno", key="Ap_Materno", value=g.get("Ap_Materno", ""), on_change=to_upper, args=["Ap_Materno"])
    c3.text_input("Nombres", key="Nombres", value=g.get("Nombres", ""), on_change=to_upper, args=["Nombres"])

    f_nacimiento = st.date_input("Fecha de nacimiento", value=g.get("F_Nac", None), min_value=date(1900, 1, 1), format="DD/MM/YYYY")
    
    # Edad (mantenemos lógica anterior)
    if f_nacimiento:
        delta = relativedelta(date.today(), f_nacimiento)
        st.success(f"Edad calculada: **{delta.years} Años, {delta.months} Meses, {delta.days} Días**")

    # --- CAMPOS RESTANTES ---
    # ... (selectboxes de entidad, sexo, escolaridad, ocupación igual que antes) ...
    
    # --- NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])
    with col_atras:
        if st.button("⬅️ Atrás"):
            idx = ORDEN.index(st.session_state.pagina_actual)
            st.session_state.pagina_actual = ORDEN[idx - 1]
            st.rerun()
    with col_guardar:
        if st.button("💾 Guardar registro y continuar"):
            # Recogemos los valores directamente del session_state (que ya están en mayúsculas gracias al callback)
            st.session_state.datos_completos["Paciente"] = {
                "Expediente": st.session_state.Expediente,
                "Ap_Paterno": st.session_state.Ap_Paterno,
                "Ap_Materno": st.session_state.Ap_Materno, 
                "Nombres": st.session_state.Nombres,
                "F_Nac": f_nacimiento
                # ... resto de campos
            }
            # ... navegación
            st.rerun()

if __name__ == "__main__":
    render()
