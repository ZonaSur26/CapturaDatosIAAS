import streamlit as st
import sys
from config import ORDEN

def render():
    st.title("Antecedentes Personales Patológicos")
    
    # --- CONTROL Y RECUPERACIÓN DE DATOS ---
    if "datos_completos" not in st.session_state:
        st.session_state.datos_completos = {}
        
    g = st.session_state.datos_completos.get("Antecedentes", {})

    antecedentes_lista = [
        "PREMATUREZ", "BAJO PESO AL NACER", "DIABETES MELLITUS", 
        "HIPERTENSIÓN ARTERIAL SISTÉMICA", "SOBREPESO", "OBESIDAD", "TABAQUISMO",
        "DESNUTRICIÓN", "ENFERMEDAD RENAL CRÓNICA", "EPOC", 
        "VIH/SIDA", "INMUNOSUPRESIÓN", "CANCER"
    ]

    # Contenedor visual limpio
    with st.container(border=True):
        st.subheader("Seleccione los antecedentes presentes")

        # Layout en 2 columnas
        col1, col2 = st.columns(2)
        mitad = (len(antecedentes_lista) + 1) // 2
        
        antecedentes_seleccionados = {}
        
        # Columna 1
        with col1:
            for item in antecedentes_lista[:mitad]:
                # Recuperamos el valor previo (por defecto "NO")
                valor_previo = g.get(item, "NO") == "SÍ"
                antecedentes_seleccionados[item] = st.checkbox(item, key=f"ant_{item}", value=valor_previo)
        
        # Columna 2
        with col2:
            for item in antecedentes_lista[mitad:]:
                valor_previo = g.get(item, "NO") == "SÍ"
                antecedentes_seleccionados[item] = st.checkbox(item, key=f"ant_{item}", value=valor_previo)

        st.markdown("---")
        
        # --- LÓGICA REACTIVA DEL CAMPO OTRO ---
        valor_otro_previo = g.get("OTRO_CHECK", "NO") == "SÍ"
        es_otro = st.checkbox("OTRO", key="k_check_otro", value=valor_otro_previo)
        
        otro_texto_ingresado = ""
        if es_otro:
            # Si existía un texto guardado previamente que no sea "NO APLICA", lo precarga
            texto_previo = g.get("OTRO_TEXTO", "")
            if texto_previo == "NO APLICA":
                texto_previo = ""
                
            otro_texto_ingresado = st.text_input(
                "Especifique el otro antecedente:", 
                key="k_otro_text", 
                value=texto_previo,
                placeholder="Ej. ASMA, CARDIOPATÍA CONGÉNITA..."
            )

    # --- FUNCIÓN DE GUARDADO CENTRALIZADA ---
    def guardar_antecedentes():
        # Mapeamos los booleanos de los checkboxes a texto "SÍ" o "NO"
        datos_formateados = {k: ("SÍ" if v is True else "NO") for k, v in antecedentes_seleccionados.items()}
        
        if es_otro:
            datos_formateados["OTRO_CHECK"] = "SÍ"
            # Si el usuario escribió algo, lo limpia y pasa a mayúsculas. Si no, guarda vacío.
            datos_formateados["OTRO_TEXTO"] = str(otro_texto_ingresado).upper().strip() if otro_texto_ingresado else ""
        else:
            datos_formateados["OTRO_CHECK"] = "NO"
            datos_formateados["OTRO_TEXTO"] = "NO APLICA"
            
        st.session_state.datos_completos["Antecedentes"] = datos_formateados

    # --- NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])

    with col_atras:
        if st.button("⬅️ Atrás"):
            guardar_antecedentes()
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx > 0:
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()

    with col_guardar:
        if st.button("💾 Guardar registro y continuar"):
            guardar_antecedentes()
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx < len(ORDEN) - 1:
                st.session_state.pagina_actual = ORDEN[idx + 1]
                st.rerun()

if __name__ == "__main__":
    render()
