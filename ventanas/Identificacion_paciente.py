import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from config import ORDEN

def render():
    st.title("Identificación del Paciente")

    # --- RECUPERACIÓN DE DATOS GUARDADOS ---
    g = st.session_state.datos_completos.get("Paciente", {})

    # Listas de datos
    estados = [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", 
        "Chihuahua", "Coahuila", "Colima", "Ciudad de México", "Durango", "Guanajuato", 
        "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", 
        "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", 
        "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
        "Veracruz", "Yucatán", "Zacatecas"
    ]
    
    paises = sorted([
        "Alemania", "Argentina", "Belice", "Bolivia", "Brasil", "Canadá", "Chile", 
        "Colombia", "Costa Rica", "Cuba", "Ecuador", "El Salvador", "Estados Unidos", 
        "Guatemala", "Haití", "Honduras", "México", "Nicaragua", "Panamá", "Paraguay", 
        "Perú", "República Dominicana", "Uruguay", "Venezuela"
    ])

    # --- DATOS GENERALES ---
    st.subheader("Datos Generales")
    expediente = st.text_input("Nº de expediente", value=g.get("Expediente", ""), placeholder="Ej. 123456")
    
    c1, c2, c3 = st.columns(3)
    with c1: ap_paterno = st.text_input("Apellido Paterno", value=g.get("Ap_Paterno", ""))
    with c2: ap_materno = st.text_input("Apellido Materno", value=g.get("Ap_Materno", ""))
    with c3: nombres = st.text_input("Nombres", value=g.get("Nombres", ""))

    c_fec, c_ed = st.columns(2)
    with c_fec:
        # Nota: date_input requiere None o un objeto date. Para persistencia, lo ideal es guardar el string y convertirlo.
        f_nacimiento = st.date_input("Fecha de nacimiento", value=None, min_value=date(1900, 1, 1), format="DD/MM/YYYY")
    
    with c_ed:
        edad_str = ""
        if f_nacimiento:
            delta = relativedelta(date.today(), f_nacimiento)
            edad_str = f"{delta.years} Años, {delta.months} Meses, {delta.days} Días"
            st.success(f"Edad calculada: **{edad_str}**")
        else:
            st.info("La edad se calculará al seleccionar la fecha")

    c_s1, c_s2 = st.columns(2)
    with c_s1:
        entidad_nac = st.selectbox("Entidad de nacimiento", estados, index=estados.index(g["Entidad_Nac"]) if g.get("Entidad_Nac") in estados else None, placeholder="Seleccione...")
        sexo = st.selectbox("Sexo", ["Hombre", "Mujer"], index=["Hombre", "Mujer"].index(g["Sexo"]) if g.get("Sexo") in ["Hombre", "Mujer"] else None, placeholder="Seleccione...")
    with c_s2:
        lista_esc = ["Sin estudios", "Primaria incompleta", "Primaria terminada", "Secundaria incompleta", "Secundaria terminada", "Preparatoria incompleta", "Preparatoria terminada", "Licenciatura incompleta", "Licenciatura terminada", "Posgrado", "Especialidad", "Maestría", "Doctorado", "Se desconoce"]
        escolaridad = st.selectbox("Escolaridad", lista_esc, index=lista_esc.index(g["Escolaridad"]) if g.get("Escolaridad") in lista_esc else None, placeholder="Seleccione nivel...")
        lista_ocu = ["Campesino", "Chofer", "Comerciante", "Dentista", "Desempleado", "Empleado", "Enfermera", "Estudiante", "Gerente", "Hogar", "Jubilado", "Laboratorista", "Maestro", "Médico", "Otros oficios", "Otro Profesionista", "Otro trabajador de salud", "Se ignora", "No aplica"]
        ocupacion = st.selectbox("Ocupación", lista_ocu, index=lista_ocu.index(g["Ocupacion"]) if g.get("Ocupacion") in lista_ocu else None, placeholder="Seleccione ocupación...")

    # --- AUTODSCRIPCIÓN CULTURAL ---
    st.subheader("Autoadscripción Cultural")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        indigena = st.radio("¿Se reconoce como indígena?", ["No", "Sí", "Se desconoce"], index=["No", "Sí", "Se desconoce"].index(g.get("Indigena", "No")), horizontal=True)
    with col_c2:
        habla_lengua = st.radio("¿Habla alguna lengua indígena?", ["No", "Sí", "Se desconoce"], index=["No", "Sí", "Se desconoce"].index(g.get("Habla_Lengua", "No")), horizontal=True)
    
    lengua_especifica = st.text_input("¿Qué lengua indígena habla?", value=g.get("Lengua_Específica", "")) if habla_lengua == "Sí" else ""

    # --- INFORMACIÓN MIGRATORIA ---
    st.subheader("Información Migratoria")
    es_migrante = st.radio("¿El paciente es migrante?", ["No", "Sí"], index=["No", "Sí"].index(g.get("Es_Migrante", "No")))

    if es_migrante == "Sí":
        st.markdown("---")
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            nac = st.selectbox("País de nacionalidad", paises, index=paises.index(g["Nacionalidad"]) if g.get("Nacionalidad") in paises else None, placeholder="Seleccione...")
            orig = st.selectbox("País de origen", paises, index=paises.index(g["Origen"]) if g.get("Origen") in paises else None, placeholder="Seleccione...")
        with c_m2:
            st.markdown("**Países en tránsito:**")
            t1 = st.selectbox("País de tránsito 1", paises, index=paises.index(g["T1"]) if g.get("T1") in paises else None, placeholder="Seleccione...")
            # ... (puedes replicar para T2, T3, T4 siguiendo la misma lógica)

    # --- BOTONES DE NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])

    with col_atras:
        if st.button("⬅️ Atrás"):
            idx = ORDEN.index(st.session_state.pagina_actual)
            st.session_state.pagina_actual = ORDEN[idx - 1]
            st.rerun()

    with col_guardar:
        if st.button("💾 Guardar registro y continuar"):
            if not all([expediente, nombres, ap_paterno]):
                st.error("Por favor, completa los campos obligatorios.")
            else:
                st.session_state.datos_completos["Paciente"] = {
                    "Expediente": expediente, "Ap_Paterno": ap_paterno, "Ap_Materno": ap_materno, 
                    "Nombres": nombres, "Entidad_Nac": entidad_nac, "Sexo": sexo,
                    "Escolaridad": escolaridad, "Ocupacion": ocupacion, "Indigena": indigena,
                    "Habla_Lengua": habla_lengua, "Lengua_Específica": lengua_especifica,
                    "Es_Migrante": es_migrante
                }
                idx = ORDEN.index(st.session_state.pagina_actual)
                if idx < len(ORDEN) - 1:
                    st.session_state.pagina_actual = ORDEN[idx + 1]
                    st.rerun()

if __name__ == "__main__":
    render()
