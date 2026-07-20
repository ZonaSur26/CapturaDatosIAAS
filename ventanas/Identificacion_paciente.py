import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
# Asegúrate de que tu archivo config.py contenga la variable ORDEN
from config import ORDEN

def render():
    st.title("Identificación del Paciente")

    # --- RECUPERACIÓN DE DATOS GUARDADOS ---
    g = st.session_state.datos_completos.get("Paciente", {})

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
    expediente = st.text_input("Nº de expediente", value=g.get("Expediente", ""))
    
    c1, c2, c3 = st.columns(3)
    ap_paterno = c1.text_input("Apellido Paterno", value=g.get("Ap_Paterno", ""))
    ap_materno = c2.text_input("Apellido Materno", value=g.get("Ap_Materno", ""))
    nombres = c3.text_input("Nombres", value=g.get("Nombres", ""))

    f_nacimiento = st.date_input("Fecha de nacimiento", value=g.get("F_Nac", None), min_value=date(1900, 1, 1), format="DD/MM/YYYY")
    
    # --- AUTODSCRIPCIÓN CULTURAL ---
    st.subheader("Autoadscripción Cultural")
    col_c1, col_c2 = st.columns(2)
    
    indigena = col_c1.radio(
        "¿Se reconoce como indígena?", 
        ["No", "Sí", "Se desconoce"], 
        index=["No", "Sí", "Se desconoce"].index(g.get("Indigena", "No")), 
        horizontal=True
    )
    
    habla_lengua = col_c2.radio(
        "¿Habla alguna lengua indígena?", 
        ["No", "Sí", "Se desconoce"], 
        index=["No", "Sí", "Se desconoce"].index(g.get("Habla_Lengua", "No")), 
        horizontal=True
    )

    # --- INFORMACIÓN MIGRATORIA ---
    st.subheader("Información Migratoria")
    es_migrante = st.radio("¿El paciente es migrante?", ["No", "Sí"], index=["No", "Sí"].index(g.get("Es_Migrante", "No")))

    t1, t2, t3, t4 = None, None, None, None
    if es_migrante == "Sí":
        c_m1, c_m2 = st.columns(2)
        nacionalidad = c_m1.selectbox("País de nacionalidad", paises, index=paises.index(g["Nacionalidad"]) if g.get("Nacionalidad") in paises else None)
        origen = c_m1.selectbox("País de origen", paises, index=paises.index(g["Origen"]) if g.get("Origen") in paises else None)
        
        c_m2.markdown("**Países en tránsito:**")
        t1 = c_m2.selectbox("País de tránsito 1", paises, index=paises.index(g.get("T1", "")) if g.get("T1") in paises else None)
        t2 = c_m2.selectbox("País de tránsito 2", paises, index=paises.index(g.get("T2", "")) if g.get("T2") in paises else None)
        t3 = c_m2.selectbox("País de tránsito 3", paises, index=paises.index(g.get("T3", "")) if g.get("T3") in paises else None)
        t4 = c_m2.selectbox("País de tránsito 4", paises, index=paises.index(g.get("T4", "")) if g.get("T4") in paises else None)

    # --- NAVEGACIÓN ---
    if st.button("💾 Guardar registro y continuar"):
        st.session_state.datos_completos["Paciente"] = {
            "Expediente": expediente, "Ap_Paterno": ap_paterno, "Ap_Materno": ap_materno, 
            "Nombres": nombres, "F_Nac": f_nacimiento, "Indigena": indigena,
            "Habla_Lengua": habla_lengua, "Lengua_Específica": lengua_especifica,
            "Es_Migrante": es_migrante, "Nacionalidad": nacionalidad if es_migrante=="Sí" else None,
            "T1": t1, "T2": t2, "T3": t3, "T4": t4
        }
        idx = ORDEN.index(st.session_state.pagina_actual)
        if idx < len(ORDEN) - 1:
            st.session_state.pagina_actual = ORDEN[idx + 1]
            st.rerun()

if __name__ == "__main__":
    render()
