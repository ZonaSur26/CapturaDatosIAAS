import streamlit as st
import sys
from datetime import date
from dateutil.relativedelta import relativedelta

def render():
    st.title("Identificación del Paciente")

    # Listas de datos
    estados = [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", 
        "Chihuahua", "Coahuila", "Colima", "Ciudad de México", "Durango", "Guanajuato", 
        "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", 
        "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", 
        "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
        "Veracruz", "Yucatán", "Zacatecas"
    ]
    
    paises = sorted(["Alemania", "Argentina", "Belice", "Bolivia", "Brasil", "Canadá", "Chile", 
                     "Colombia", "Costa Rica", "Cuba", "Ecuador", "El Salvador", "Estados Unidos", 
                     "Guatemala", "Haití", "Honduras", "México", "Nicaragua", "Panamá", "Paraguay", 
                     "Perú", "República Dominicana", "Uruguay", "Venezuela"])

    # --- DATOS GENERALES ---
    st.subheader("Datos Generales")
    expediente = st.text_input("Nº de expediente", placeholder="Ej. 123456")
    
    c1, c2, c3 = st.columns(3)
    with c1: ap_paterno = st.text_input("Apellido Paterno")
    with c2: ap_materno = st.text_input("Apellido Materno")
    with c3: nombres = st.text_input("Nombres")

    c_fec, c_ed = st.columns(2)
    with c_fec:
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
        entidad_nac = st.selectbox("Entidad de nacimiento", estados, index=None, placeholder="Seleccione...")
        sexo = st.selectbox("Sexo", ["Hombre", "Mujer"], index=None, placeholder="Seleccione...")
    with c_s2:
        escolaridad = st.selectbox("Escolaridad", ["Sin estudios", "Primaria incompleta", "Primaria terminada", "Secundaria incompleta", "Secundaria terminada", "Preparatoria incompleta", "Preparatoria terminada", "Licenciatura incompleta", "Licenciatura terminada", "Posgrado", "Especialidad", "Maestría", "Doctorado", "Se desconoce"], index=None, placeholder="Seleccione nivel...")
        ocupacion = st.selectbox("Ocupación", ["Campesino", "Chofer", "Comerciante", "Dentista", "Desempleado", "Empleado", "Enfermera", "Estudiante", "Gerente", "Hogar", "Jubilado", "Laboratorista", "Maestro", "Médico", "Otros oficios", "Otro Profesionista", "Otro trabajador de salud", "Se ignora", "No aplica"], index=None, placeholder="Seleccione ocupación...")

    # --- AUTODSCRIPCIÓN CULTURAL ---
    st.subheader("Autoadscripción Cultural")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        indigena = st.radio("¿Se reconoce como indígena?", ["No", "Sí", "Se desconoce"], index=0, horizontal=True)
    with col_c2:
        habla_lengua = st.radio("¿Habla alguna lengua indígena?", ["No", "Sí", "Se desconoce"], index=0, horizontal=True)
    
    lengua_especifica = ""
    if habla_lengua == "Sí":
        lengua_especifica = st.text_input("¿Qué lengua indígena habla?")

    # --- INFORMACIÓN MIGRATORIA ---
    st.subheader("Información Migratoria")
    es_migrante = st.radio("¿El paciente es migrante?", ["No", "Sí"], index=0)

    # --- BOTÓN DE GUARDADO ---
    if st.button("Guardar registro y continuar"):
        # Validación de campos obligatorios
        if not all([expediente, ap_paterno, nombres, f_nacimiento, entidad_nac, sexo]):
            st.error("Por favor, completa los campos obligatorios (Expediente, Nombre, Apellido, Fecha, Entidad y Sexo).")
        else:
            # Guardado centralizado
            st.session_state.datos_completos["Paciente"] = {
                "Expediente": expediente,
                "Nombre": f"{nombres} {ap_paterno} {ap_materno}",
                "Fecha_Nacimiento": f_nacimiento.strftime("%d/%m/%Y"),
                "Edad": edad_str,
                "Escolaridad": escolaridad,
                "Ocupacion": ocupacion,
                "Indigena": indigena,
                "Es_Migrante": es_migrante
            }
            
            # Navegación automática segura
            main_module = sys.modules['main']
            ORDEN = main_module.ORDEN
            indice = ORDEN.index(st.session_state.pagina_actual)
            
            if indice < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[indice + 1]
                st.success("Guardado. Redirigiendo...")
                st.rerun()

if __name__ == "__main__":
    render()
