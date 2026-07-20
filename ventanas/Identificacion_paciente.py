import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from config import ORDEN

def render():
    st.title("Identificación del Paciente")

    # 1. RECUPERAR DATOS GUARDADOS
    g = st.session_state.datos_completos.get("Paciente", {})

    # Listas de datos
    estados = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
    paises = sorted(["Alemania", "Argentina", "Belice", "Bolivia", "Brasil", "Canadá", "Chile", "Colombia", "Costa Rica", "Cuba", "Ecuador", "El Salvador", "Estados Unidos", "Guatemala", "Haití", "Honduras", "México", "Nicaragua", "Panamá", "Paraguay", "Perú", "República Dominicana", "Uruguay", "Venezuela"])

    # --- DATOS GENERALES ---
    st.subheader("Datos Generales")
    expediente = st.text_input("Nº de expediente", value=g.get("Expediente", ""), placeholder="Ej. 123456")
    
    # Nota: Para nombres, aquí extraemos las partes (esto depende de cómo los guardaste)
    # Sugerencia: guarda ap_paterno, ap_materno y nombres por separado en el futuro
    c1, c2, c3 = st.columns(3)
    with c1: ap_paterno = st.text_input("Apellido Paterno", value=g.get("Apellido_P", ""))
    with c2: ap_materno = st.text_input("Apellido Materno", value=g.get("Apellido_M", ""))
    with c3: nombres = st.text_input("Nombres", value=g.get("Nombres", ""))

    c_fec, c_ed = st.columns(2)
    with c_fec:
        # Nota: Date inputs requieren un objeto date, no un string
        f_nacimiento = st.date_input("Fecha de nacimiento", value=None, min_value=date(1900, 1, 1), format="DD/MM/YYYY")
    
    with c_ed:
        if f_nacimiento:
            delta = relativedelta(date.today(), f_nacimiento)
            st.success(f"Edad calculada: **{delta.years} Años, {delta.months} Meses, {delta.days} Días**")

    c_s1, c_s2 = st.columns(2)
    with c_s1:
        # Para selectboxes, buscamos el index del valor guardado
        entidad_nac = st.selectbox("Entidad de nacimiento", estados, index=estados.index(g["Entidad_Nac"]) if g.get("Entidad_Nac") in estados else None)
        sexo = st.selectbox("Sexo", ["Hombre", "Mujer"], index=["Hombre", "Mujer"].index(g["Sexo"]) if g.get("Sexo") in ["Hombre", "Mujer"] else None)
    with c_s2:
        lista_escolaridad = ["Sin estudios", "Primaria incompleta", "Primaria terminada", "Secundaria incompleta", "Secundaria terminada", "Preparatoria incompleta", "Preparatoria terminada", "Licenciatura incompleta", "Licenciatura terminada", "Posgrado", "Especialidad", "Maestría", "Doctorado", "Se desconoce"]
        escolaridad = st.selectbox("Escolaridad", lista_escolaridad, index=lista_escolaridad.index(g["Escolaridad"]) if g.get("Escolaridad") in lista_escolaridad else None)
        
        lista_ocupacion = ["Campesino", "Chofer", "Comerciante", "Dentista", "Desempleado", "Empleado", "Enfermera", "Estudiante", "Gerente", "Hogar", "Jubilado", "Laboratorista", "Maestro", "Médico", "Otros oficios", "Otro Profesionista", "Otro trabajador de salud", "Se ignora", "No aplica"]
        ocupacion = st.selectbox("Ocupación", lista_ocupacion, index=lista_ocupacion.index(g["Ocupacion"]) if g.get("Ocupacion") in lista_ocupacion else None)

    # --- AUTODSCRIPCIÓN CULTURAL ---
    indigena = st.radio("¿Se reconoce como indígena?", ["No", "Sí", "Se desconoce"], index=["No", "Sí", "Se desconoce"].index(g.get("Indigena", "No")), horizontal=True)
    habla_lengua = st.radio("¿Habla alguna lengua indígena?", ["No", "Sí", "Se desconoce"], index=["No", "Sí", "Se desconoce"].index(g.get("Habla_Lengua", "No")), horizontal=True)
    lengua_especifica = st.text_input("¿Qué lengua indígena habla?", value=g.get("Lengua_Específica", "")) if habla_lengua == "Sí" else ""

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
            st.session_state.datos_completos["Paciente"] = {
                "Expediente": expediente, "Apellido_P": ap_paterno, "Apellido_M": ap_materno, 
                "Nombres": nombres, "Entidad_Nac": entidad_nac, "Sexo": sexo,
                "Escolaridad": escolaridad, "Ocupacion": ocupacion, "Indigena": indigena,
                "Habla_Lengua": habla_lengua, "Lengua_Específica": lengua_especifica
            }
            idx = ORDEN.index(st.session_state.pagina_actual)
            st.session_state.pagina_actual = ORDEN[idx + 1]
            st.rerun()
