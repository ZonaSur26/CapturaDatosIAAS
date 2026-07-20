import streamlit as st



def boton_navegacion(nombre_pagina_actual):

    """

    Crea un contenedor con los botones de acción al final de cada página.

    """

    st.divider()

    col_atras, col_guardar = st.columns([1, 4])

    

    # Lógica del botón Atrás

    with col_atras:

        # Obtener índice actual

        from main import ORDEN # Importamos la lista de orden

        idx = ORDEN.index(nombre_pagina_actual)

        

        if idx > 0:

            if st.button("⬅️ Atrás"):

                st.session_state.pagina_actual = ORDEN[idx - 1]

                st.rerun()



    # Aquí iría tu botón de guardar original

    with col_guardar:

        if st.button("💾 Guardar cambios"):

            st.success(f"Datos de {nombre_pagina_actual} guardados correctamente.")

