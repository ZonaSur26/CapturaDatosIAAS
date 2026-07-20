import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from config import ORDEN

# Función para forzar mayúsculas en tiempo real
def to_upper(key):
    st.session_state[key] = str(st.session_state[key]).upper()

def render():
    st.title("Identificación del Paciente")

    # --- RECUPERACIÓN DE DATOS ---
    g = st.session_state.datos_completos.get("Paciente", {})

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

    c_fec, c_ed = st.columns(2)
    f_nacimiento = c_fec.date_input("Fecha de nacimiento", value=g.get("F_Nac", None), min_value=date(1900, 1, 1), format="DD/MM/YYYY")
    if f_nacimiento:
        delta = relativedelta(date.today(), f_nacimiento)
        c_ed.success(f"Edad calculada: **{delta.years} Años, {delta.months} Meses, {delta.days} Días**")

    c_s1, c_s2 = st.columns(2)
    entidad_nac = c_s1.selectbox("Entidad de nacimiento", estados, index=estados.index(g["Entidad_Nac"]) if g.get("Entidad_Nac") in estados else None)
    sexo = c_s1.selectbox("Sexo", ["Hombre", "Mujer"], index=["Hombre", "Mujer"].index(g["Sexo"]) if g.get("Sexo") in ["Hombre", "Mujer"] else None)
    escolaridad = c_s2.selectbox("Escolaridad", lista_esc, index=lista_esc.index(g["Escolaridad"]) if g.get("Escolaridad") in lista_esc else None)
    ocupacion = c_s2.selectbox("Ocupación", lista_ocu, index=lista_ocu.index(g["Ocupacion"]) if g.get("Ocupacion") in lista_ocu else None)

    # --- AUTODSCRIPCIÓN CULTURAL ---
    st.subheader("Autoadscripción Cultural")
    col_c1, col_c2 = st.columns(2)
    indigena = col_c1.radio("¿Se reconoce como indígena?", ["No", "Sí", "Se desconoce"], index=["No", "Sí", "Se desconoce"].index(g.get("Indigena", "No")), horizontal=True)
    habla_lengua = col_c2.radio("¿Habla alguna lengua indígena?", ["No", "Sí", "Se desconoce"], index=["No", "Sí", "Se desconoce"].index(g.get("Habla_Lengua", "No")), horizontal=True)

    # --- INFORMACIÓN MIGRATORIA ---
    st.subheader("Información Migratoria")
    es_migrante = st.radio("¿El paciente es migrante?", ["No", "Sí"], index=["No", "Sí"].index(g.get("Es_Migrante", "No")))
    
    t1, t2, t3, t4, nacionalidad, origen = None, None, None, None, None, None
    if es_migrante == "Sí":
        c_m1, c_m2 = st.columns(2)
        nacionalidad = c_m1.selectbox("País de nacionalidad", paises, index=paises.index(g.get("Nacionalidad", "")) if g.get("Nacionalidad") in paises else None)
        origen = c_m1.selectbox("País de origen", paises, index=paises.index(g.get("Origen", "")) if g.get("Origen") in paises else None)
        c_m2.markdown("**Países en tránsito:**")
        t1 = c_m2.selectbox("País de tránsito 1", paises, index=paises.index(g.get("T1", "")) if g.get("T1") in paises else None)
        t2 = c_m2.selectbox("País de tránsito 2", paises, index=paises.index(g.get("T2", "")) if g.get("T2") in paises else None)
        t3 = c_m2.selectbox("País de tránsito 3", paises, index=paises.index(g.get("T3", "")) if g.get("T3") in paises else None)
        t4 = c_m2.selectbox("País de tránsito 4", paises, index=paises.index(g.get("T4", "")) if g.get("T4") in paises else None)

    # --- NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])
    if col_atras.button("⬅️ Atrás"):
        idx = ORDEN.index(st.session_state.pagina_actual)
        st.session_state.pagina_actual = ORDEN[idx - 1]
        st.rerun()
        
    if col_guardar.button("💾 Guardar registro y continuar"):
        st.session_state.datos_completos["Paciente"] = {
            "Expediente": st.session_state.Expediente, "Ap_Paterno": st.session_state.Ap_Paterno, 
            "Ap_Materno": st.session_state.Ap_Materno, "Nombres": st.session_state.Nombres,
            "F_Nac": f_nacimiento, "Entidad_Nac": entidad_nac, "Sexo": sexo,
            "Escolaridad": escolaridad, "Ocupacion": ocupacion, "Indigena": indigena,
            "Habla_Lengua": habla_lengua, "Es_Migrante": es_migrante,
            "Nacionalidad": nacionalidad, "Origen": origen, "T1": t1, "T2": t2, "T3": t3, "T4": t4
        }
        idx = ORDEN.index(st.session_state.pagina_actual)
        if idx < len(ORDEN) - 1:
            st.session_state.pagina_actual = ORDEN[idx + 1]
            st.rerun()

if __name__ == "__main__":
    render()
