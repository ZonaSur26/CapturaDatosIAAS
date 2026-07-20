import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from config import ORDEN

def render():
    st.title("Identificación del Paciente")

    # --- CONTROL Y RECUPERACIÓN DE DATOS ---
    if "datos_completos" not in st.session_state:
        st.session_state.datos_completos = {"Unidad": {}, "Paciente": {}}
        
    g = st.session_state.datos_completos.get("Paciente", {})

    # Catálogos de prellenado
    estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
    lista_esc = ["Sin estudios", "Primaria incompleta", "Primaria terminada", "Secundaria incompleta", "Secundaria terminada", "Preparatoria incompleta", "Preparatoria terminada", "Licenciatura incompleta", "Licenciatura terminada", "Posgrado", "Especialidad", "Maestría", "Doctorado", "Se desconoce"]
    lista_ocu = ["Campesino", "Chofer", "Comerciante", "Dentista", "Desempleado", "Empleado", "Enfermera", "Estudiante", "Gerente", "Hogar", "Jubilado", "Laboratorista", "Maestro", "Médico", "Otros oficios", "Otro Profesionista", "Otro trabajador de salud", "Se ignora", "No aplica"]
    paises = sorted(["Alemania", "Argentina", "Belice", "Bolivia", "Brasil", "Canadá", "Chile", "Colombia", "Costa Rica", "Cuba", "Ecuador", "El Salvador", "Estados Unidos", "Guatemala", "Haití", "Honduras", "México", "Nicaragua", "Panamá", "Paraguay", "Perú", "República Dominicana", "Uruguay", "Venezuela"])

    # CAMBIO CRÍTICO: Usamos st.container en lugar de st.form para permitir reactividad instantánea
    with st.container(border=True):
        
        # --- DATOS GENERALES ---
        st.subheader("Datos Generales")
        st.text_input("Nº de expediente", key="Expediente", value=g.get("Expediente", ""), placeholder="Ej. 123456")
        
        c1, c2, c3 = st.columns(3)
        c1.text_input("Apellido Paterno", key="Ap_Paterno", value=g.get("Ap_Paterno", ""))
        c2.text_input("Apellido Materno", key="Ap_Materno", value=g.get("Ap_Materno", ""))
        c3.text_input("Nombres", key="Nombres", value=g.get("Nombres", ""))

        c_fec, c_ed = st.columns(2)
        f_nacimiento = c_fec.date_input("Fecha de nacimiento", value=g.get("F_Nac", None), min_value=date(1900, 1, 1), format="DD/MM/YYYY")
        
        # --- LÓGICA DE EDAD INTELIGENTE ---
        edad_inteligente = ""
        if f_nacimiento:
            delta = relativedelta(date.today(), f_nacimiento)
            if delta.years >= 1:
                edad_inteligente = f"{delta.years} Años"
            elif delta.months >= 1:
                edad_inteligente = f"{delta.months} Meses"
            else:
                edad_inteligente = f"{delta.days} Días"
            c_ed.success(f"Edad calculada: **{edad_inteligente}**")

        c_s1, c_s2 = st.columns(2)
        entidad_nac = c_s1.selectbox("Entidad de nacimiento", estados, index=estados.index(g["Entidad_Nac"]) if g.get("Entidad_Nac") in estados else None)
        sexo = c_s1.selectbox("Sexo", ["Hombre", "Mujer"], index=["Hombre", "Mujer"].index(g["Sexo"]) if g.get("Sexo") in ["Hombre", "Mujer"] else None)
        escolaridad = c_s2.selectbox("Escolaridad", lista_esc, index=lista_esc.index(g["Escolaridad"]) if g.get("Escolaridad") in lista_esc else None)
        ocupacion = c_s2.selectbox("Ocupación", lista_ocu, index=lista_ocu.index(g["Ocupacion"]) if g.get("Ocupacion") in lista_ocu else None)

        # --- AUTOADSCRIPCIÓN CULTURAL ---
        st.subheader("Autoadscripción Cultural")
        col_c1, col_c2 = st.columns(2)
        indigena = col_c1.radio("¿Se reconoce como indígena?", ["No", "Sí", "Se desconoce"], index=["No", "Sí", "Se desconoce"].index(g.get("Indigena", "No")), horizontal=True)
        habla_lengua = col_c2.radio("¿Habla alguna lengua indígena?", ["No", "Sí", "Se desconoce"], index=["No", "Sí", "Se desconoce"].index(g.get("Habla_Lengua", "No")), horizontal=True)

        # --- INFORMACIÓN MIGRATORIA ---
        st.subheader("Información Migratoria")
        
        # Al estar en un container, los cambios en este radio disparan la pantalla inmediatamente
        es_migrante = st.radio(
            "¿El paciente es migrante?", 
            ["No", "Sí"], 
            index=["No", "Sí"].index(g.get("Es_Migrante", "No")),
            key="k_es_migrante"
        )
        
        t1, t2, t3, t4, nacionalidad, origen = None, None, None, None, None, None
        
        # Ahora la condición se lee perfectamente en tiempo real
        if es_migrante == "Sí":
            c_m1, c_m2 = st.columns(2)
            nacionalidad = c_m1.selectbox("País de nacionalidad", paises, index=paises.index(g.get("Nacionalidad", "")) if g.get("Nacionalidad") in paises else None)
            origen = c_m1.selectbox("País de origen", paises, index=paises.index(g.get("Origen", "")) if g.get("Origen") in paises else None)
            
            c_m2.markdown("**Países en tránsito:**")
            t1 = c_m2.selectbox("País de tránsito 1", paises, index=paises.index(g.get("T1", "")) if g.get("T1") in paises else None)
            t2 = c_m2.selectbox("País de tránsito 2", paises, index=paises.index(g.get("T2", "")) if g.get("T2") in paises else None)
            t3 = c_m2.selectbox("País de tránsito 3", paises, index=paises.index(g.get("T3", "")) if g.get("T3") in paises else None)
            t4 = c_m2.selectbox("País de tránsito 4", paises, index=paises.index(g.get("T4", "")) if g.get("T4") in paises else None)

        st.write("") # Espaciador estético
        
        # Botón normal de Streamlit (sin los bloqueos de st.form_submit_button)
        submit = st.button("💾 Guardar registro y continuar")
        
        if submit:
            def clean(key):
                val = st.session_state.get(key, "")
                return str(val).upper().strip() if val else ""

            st.session_state.datos_completos["Paciente"] = {
                "Expediente": clean("Expediente"), 
                "Ap_Paterno": clean("Ap_Paterno"), 
                "Ap_Materno": clean("Ap_Materno"), 
                "Nombres": clean("Nombres"),
                "F_Nac": f_nacimiento,  
                "Edad": edad_inteligente, 
                "Entidad_Nac": clean("Entidad_Nac") if entidad_nac else "", 
                "Sexo": clean("Sexo") if sexo else "",
                "Escolaridad": clean("Escolaridad") if escolaridad else "", 
                "Ocupacion": clean("Ocupacion") if ocupacion else "", 
                "Indigena": clean("Indigena") if indigena else "NO",
                "Habla_Lengua": clean("Habla_Lengua") if habla_lengua else "NO", 
                "Es_Migrante": clean("k_es_migrante"),
                "Nacionalidad": clean("Nacionalidad") if nacionalidad else "", 
                "Origen": clean("Origen") if origen else "", 
                "T1": clean("T1") if t1 else "", 
                "T2": clean("T2") if t2 else "", 
                "T3": clean("T3") if t3 else "", 
                "T4": clean("T4") if t4 else ""
            }
            
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[idx + 1]
                st.rerun()

    # Botón Atrás externo
    if st.button("⬅️ Atrás"):
        idx = ORDEN.index(st.session_state.pagina_actual)
        if idx > 0:
            st.session_state.pagina_actual = ORDEN[idx - 1]
            st.rerun()

if __name__ == "__main__":
    render()
