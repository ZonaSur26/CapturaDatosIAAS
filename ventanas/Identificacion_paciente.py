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

    # Funciones auxiliares para buscar índices ignorando mayúsculas/minúsculas
    def buscar_indice(lista, valor_guardado):
        if not valor_guardado:
            return None
        lista_minusculas = [str(x).lower() for x in lista]
        v_clean = str(valor_guardado).lower().strip()
        if v_clean in lista_minusculas:
            return lista_minusculas.index(v_clean)
        return None

    # Con contenedor con borde para permitir reactividad dinámica limpia
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
        entidad_nac = c_s1.selectbox("Entidad de nacimiento", estados, index=buscar_indice(estados, g.get("Entidad_Nac")))
        sexo = c_s1.selectbox("Sexo", ["Hombre", "Mujer"], index=buscar_indice(["Hombre", "Mujer"], g.get("Sexo")))
        escolaridad = c_s2.selectbox("Escolaridad", lista_esc, index=buscar_indice(lista_esc, g.get("Escolaridad")))
        ocupacion = c_s2.selectbox("Ocupación", lista_ocu, index=buscar_indice(lista_ocu, g.get("Ocupacion")))

        # --- AUTOADSCRIPCIÓN CULTURAL ---
        st.subheader("Autoadscripción Cultural")
        col_c1, col_c2 = st.columns(2)
        indigena = col_c1.radio("¿Se reconoce como indígena?", ["No", "Sí", "Se desconoce"], index=buscar_indice(["No", "Sí", "Se desconoce"], g.get("Indigena", "No")), horizontal=True)
        habla_lengua = col_c2.radio("¿Habla alguna lengua indígena?", ["No", "Sí", "Se desconoce"], index=buscar_indice(["No", "Sí", "Se desconoce"], g.get("Habla_Lengua", "No")), horizontal=True)

        # --- INFORMACIÓN MIGRATORIA ---
        st.subheader("Información Migratoria")
        
        es_migrante = st.radio(
            "¿El paciente es migrante?", 
            ["No", "Sí"], 
            index=buscar_indice(["No", "Sí"], g.get("Es_Migrante", "No")),
            key="k_es_migrante"
        )
        
        t1, t2, t3, t4, nacionalidad, origen = None, None, None, None, None, None
        viajo_3m, hosp_transito, pais_hosp = None, None, None
        
        if es_migrante == "Sí":
            c_m1, c_m2 = st.columns(2)
            nacionalidad = c_m1.selectbox("País de nacionalidad", paises, index=buscar_indice(paises, g.get("Nacionalidad")))
            origen = c_m1.selectbox("País de origen", paises, index=buscar_indice(paises, g.get("Origen")))
            
            c_m2.markdown("**Países en tránsito:**")
            t1 = c_m2.selectbox("País de tránsito 1", paises, index=buscar_indice(paises, g.get("T1")))
            t2 = c_m2.selectbox("País de tránsito 2", paises, index=buscar_indice(paises, g.get("T2")))
            t3 = c_m2.selectbox("País de tránsito 3", paises, index=buscar_indice(paises, g.get("T3")))
            t4 = c_m2.selectbox("País de tránsito 4", paises, index=buscar_indice(paises, g.get("T4")))

            st.divider()
            
            # --- NUEVAS VARIABLES MIGRATORIAS ---
            col_mig1, col_mig2 = st.columns(2)
            
            viajo_3m = col_mig1.radio(
                "¿Ha viajado a otro país durante los últimos 3 meses?",
                ["No", "Sí"],
                index=buscar_indice(["No", "Sí"], g.get("Viajo_3M", "No")),
                horizontal=True,
                key="k_viajo_3m"
            )
            
            hosp_transito = col_mig2.radio(
                "¿Durante su tránsito estuvo hospitalizado?",
                ["No", "Sí"],
                index=buscar_indice(["No", "Sí"], g.get("Hosp_Transito", "No")),
                horizontal=True,
                key="k_hosp_transito"
            )
            
            if hosp_transito == "Sí":
                pais_hosp = st.selectbox(
                    "¿En qué país estuvo hospitalizado?",
                    paises,
                    index=buscar_indice(paises, g.get("Pais_Hosp")),
                    key="k_pais_hosp",
                    placeholder="Seleccione..."
                )

        st.write("") 
        submit = st.button("💾 Guardar registro y continuar")
        
        if submit:
            def clean(key):
                val = st.session_state.get(key, "")
                return str(val).upper().strip() if val else ""

            def clean_val(val):
                return str(val).upper().strip() if val else ""

            st.session_state.datos_completos["Paciente"] = {
                "Expediente": clean("Expediente"), 
                "Ap_Paterno": clean("Ap_Paterno"), 
                "Ap_Materno": clean("Ap_Materno"), 
                "Nombres": clean("Nombres"),
                "F_Nac": f_nacimiento,  
                "Edad": edad_inteligente, 
                "Entidad_Nac": clean_val(entidad_nac), 
                "Sexo": clean_val(sexo),
                "Escolaridad": clean_val(escolaridad), 
                "Ocupacion": clean_val(ocupacion), 
                "Indigena": clean_val(indigena),
                "Habla_Lengua": clean_val(habla_lengua), 
                "Es_Migrante": clean_val(es_migrante),
                "Nacionalidad": clean_val(nacionalidad), 
                "Origen": clean_val(origen), 
                "T1": clean_val(t1), 
                "T2": clean_val(t2), 
                "T3": clean_val(t3), 
                "T4": clean_val(t4),
                # --- MAPEO DE NUEVAS COLUMNAS (W, X, Y) PARA UTILS.PY ---
                "Viajo_3M": clean_val(viajo_3m),        # Columna W
                "Hosp_Transito": clean_val(hosp_transito), # Columna X
                "Pais_Hosp": clean_val(pais_hosp)      # Columna Y
            }
            
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[idx + 1]
                st.rerun()

    if st.button("⬅️ Atrás"):
        idx = ORDEN.index(st.session_state.pagina_actual)
        if idx > 0:
            st.session_state.pagina_actual = ORDEN[idx - 1]
            st.rerun()

if __name__ == "__main__":
    render()
