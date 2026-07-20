# --- 3. LÓGICA DE GUARDADO ---
    def guardar():
        st.session_state.datos_completos["IAAS"] = {
            "Tipo_IAAS": st.session_state.k_tipo_iaas,
            "Tipo_Deteccion": st.session_state.k_deteccion,
            "Brote": st.session_state.k_brote,
            "Otro_IAAS": st.session_state.get("k_otro_iaas", "")
        }
        st.session_state.habilitar_microbiologia = (st.session_state.k_deteccion == "Confirmada por laboratorio")

    # --- 4. NAVEGACIÓN ---
    st.divider()
    col_atras, col_guardar = st.columns([1, 4])
    
    with col_atras:
        if st.button("⬅️ Atrás"):
            guardar()
            idx = ORDEN.index(st.session_state.pagina_actual)
            if idx > 0:
                st.session_state.pagina_actual = ORDEN[idx - 1]
                st.rerun()

    with col_guardar:
        if st.button("💾 Guardar registro y continuar"):
            if not st.session_state.k_tipo_iaas or not st.session_state.k_deteccion:
                st.error("Por favor, selecciona los campos obligatorios.")
            else:
                guardar()
                idx = ORDEN.index(st.session_state.pagina_actual)
                if idx < len(ORDEN) - 1:
                    st.session_state.pagina_actual = ORDEN[idx + 1]
                    st.rerun()

if __name__ == "__main__":
    render()
