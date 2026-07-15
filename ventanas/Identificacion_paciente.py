import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

def render():
    st.title("Identificación del Paciente")
    
    # Lista de estados
    estados = [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", 
        "Chihuahua", "Coahuila", "Colima", "Ciudad de México", "Durango", "Guanajuato", 
        "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", 
        "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", 
        "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", 
        "Veracruz", "Yucatán", "Zacatecas"
    ]

    with st.form("form_paciente"):
        st.subheader("Datos Generales")
        expediente = st.text_input("Nº de expediente", placeholder="Ej. 123456")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            ap_paterno = st.text_input("Apellido Paterno")
        with col2:
            ap_materno = st.text_input("Apellido Materno")
        with col3:
            nombres = st.text_input("Nombres")

        col_fecha, col_edad = st.columns([1, 1])
        with col_fecha:
            # Usamos value=None para que inicie limpio
            f_nacimiento = st.date_input("Fecha de nacimiento (dd/mm/aaaa)", value=None, min_value=date(1900, 1, 1))
        
        with col_edad:
            # Lógica para mostrar la edad solo si ya se seleccionó fecha
            if f_nacimiento:
                edad_delta = relativedelta(date.today(), f_nacimiento)
                edad_str = f"{edad_delta.years} Años, {edad_delta.months} Meses, {edad_delta.days} Días"
            else:
                edad_str = ""
            st.text_input("Edad", value=edad_str, disabled=True, placeholder="Se calculará automáticamente")

        col_select1, col_select2 = st.columns(2)
        with col_select1:
            # index=None hace que no seleccione nada por defecto
            entidad_nac = st.selectbox("Entidad de nacimiento", estados, index=None, placeholder="Seleccione un estado...")
            sexo = st.selectbox("Sexo", ["Hombre", "Mujer"], index=None, placeholder="Seleccione...")
        
        with col_select2:
            escolaridad = st.selectbox("Escolaridad", [
                "Sin estudios", "Primaria incompleta", "Primaria terminada", 
                "Secundaria incompleta", "Secundaria terminada", "Preparatoria incompleta", 
                "Preparatoria terminada", "Licenciatura incompleta", "Licenciatura terminada", 
                "Posgrado", "Especialidad", "Maestría", "Doctorado", "Se desconoce"
            ], index=None, placeholder="Seleccione nivel...")
            
            ocupacion = st.selectbox("Ocupación", [
                "Campesino", "Chofer", "Comerciante de mercado fijo o ambulante", "Dentista", 
                "Desempleado", "Empleado", "Enfermera", "Estudiante", "Gerente", "Hogar", 
                "Jubilado", "Laboratorista", "Maestro", "Médico", "Otros oficios", 
                "Otro Profesionista", "Otro trabajador de salud", "Se ignora", "No aplica"
            ], index=None, placeholder="Seleccione ocupación...")

        submit = st.form_submit_button("Guardar Paciente y Continuar")

        if submit:
            # Validación simple para asegurar campos llenos
            if not f_nacimiento or not entidad_nac or not sexo:
                st.error("Por favor, completa los campos obligatorios.")
            else:
                st.session_state.datos_paciente = {
                    "Expediente": expediente,
                    "Nombre_Completo": f"{ap_paterno} {ap_materno} {nombres}",
                    "Edad": edad_str,
                    "Entidad": entidad_nac
                }
                st.success("Información del paciente guardada.")
