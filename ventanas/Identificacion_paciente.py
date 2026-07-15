import streamlit as st
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
    
    paises = sorted([
        "Alemania", "Argentina", "Belice", "Bolivia", "Brasil", "Canadá", "Chile", 
        "Colombia", "Costa Rica", "Cuba", "Ecuador", "El Salvador", "Estados Unidos", 
        "Guatemala", "Haití", "Honduras", "México", "Nicaragua", "Panamá", "Paraguay", 
        "Perú", "República Dominicana", "Uruguay", "Venezuela"
    ])

    with st.form("form_paciente"):
        st.subheader("Datos Generales")
        expediente = st.text_input("Nº de expediente", placeholder="Ej. 123456")
        
        c1, c2, c3 = st.columns(3)
        with c1: ap_paterno = st.text_input("Apellido Paterno")
        with c2: ap_materno = st.text_input("Apellido Materno")
        with c3: nombres = st.text_input("Nombres")

        c_fec, c_ed = st.columns(2)
        with c_fec:
            f_nacimiento = st.date_input("Fecha de nacimiento (dd/mm/aaaa)", value=None, min_value=date(1900, 1, 1))
        with c_ed:
            edad_str = ""
            if f_nacimiento:
                delta = relativedelta(date.today(), f_nacimiento)
                edad_str = f"{delta.years} Años, {delta.months} Meses, {delta.days} Días"
            st.text_input("Edad", value=edad_str, disabled=True, placeholder="Se calcula automáticamente")

        c_s1, c_s2 = st.columns(2)
        with c_s1:
            entidad_nac = st.selectbox("Entidad de nacimiento", estados, index=None, placeholder="Seleccione...")
            sexo = st.selectbox("Sexo", ["Hombre", "Mujer"], index=None, placeholder="Seleccione...")
        with c_s2:
            escolaridad = st.selectbox("Escolaridad", ["Sin estudios", "Primaria incompleta", "Primaria terminada", "Secundaria incompleta", "Secundaria terminada", "Preparatoria incompleta", "Preparatoria terminada", "Licenciatura incompleta", "Licenciatura terminada", "Posgrado", "Especialidad", "Maestría", "Doctorado", "Se desconoce"], index=None, placeholder="Seleccione nivel...")
            ocupacion = st.selectbox("Ocupación", ["Campesino", "Chofer", "Comerciante", "Dentista", "Desempleado", "Empleado", "Enfermera", "Estudiante", "Gerente", "Hogar", "Jubilado", "Laboratorista", "Maestro", "Médico", "Otros oficios", "Otro Profesionista", "Otro trabajador de salud", "Se ignora", "No aplica"], index=None, placeholder="Seleccione ocupación...")

        # --- Lógica de Migrante ---
        st.subheader("Información Migratoria")
        # El on_change=st.rerun permite que al hacer clic en Sí, el formulario se actualice al instante
        es_migrante = st.radio("¿El paciente es migrante?", ["No", "Sí"], index=0, key="mig_radio", on_change=st.rerun)

        if es_migrante == "Sí":
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                nac = st.selectbox("País de nacionalidad", paises, index=None, placeholder="Seleccione...")
                orig = st.selectbox("País de origen", paises, index=None, placeholder="Seleccione...")
            with c_m2:
                st.write("Países en tránsito:")
                t1 = st.selectbox("1", paises, index=None, label_visibility="collapsed")
                t2 = st.selectbox("2", paises, index=None, label_visibility="collapsed")
                t3 = st.selectbox("3", paises, index=None, label_visibility="collapsed")
                t4 = st.selectbox("4", paises, index=None, label_visibility="collapsed")
            
            viaje = st.radio("¿Ha viajado a otro país durante los últimos 3 meses?", ["No", "Sí"])
            hosp = st.radio("¿Durante su tránsito estuvo hospitalizado?", ["No", "Sí"], key="hosp_radio", on_change=st.rerun)
            
            if hosp == "Sí":
                pais_hosp = st.selectbox("¿En qué país estuvo hospitalizado?", paises, index=None, placeholder="Seleccione país...")

        submit = st.form_submit_button("Guardar Paciente y Continuar")

        if submit:
            if not f_nacimiento or not entidad_nac or not sexo:
                st.error("Por favor, completa los campos obligatorios.")
            else:
                st.session_state.datos_paciente = {
                    "Expediente": expediente,
                    "Nombre": f"{nombres} {ap_paterno} {ap_materno}",
                    "Edad": edad_str,
                    "Es_Migrante": es_migrante
                }
                st.success("Información del paciente guardada.")
