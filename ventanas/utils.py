def enviar_a_sheets_mapeado(datos_completos):
    try:
        # ... (conexión inicial igual) ...
        
        # Acceso a los bloques
        u = datos_completos.get("Unidad", {})
        p = datos_completos.get("Paciente", {})
        
        # Mapeo según tu tabla (Fila 1)
        actualizaciones = [
            ("A1", u.get("Fecha_Captura")),
            ("B1", u.get("Unidad_Notificante")),
            ("C1", u.get("Entidad")),
            ("D1", u.get("Municipio")),
            ("E1", u.get("Jurisdiccion")),
            ("F1", u.get("Localidad")),
            ("G1", u.get("CLUES")),
            ("H1", p.get("Expediente")),
            ("I1", p.get("Apellido_Paterno")),
            ("J1", p.get("Apellido_Materno")),
            ("K1", p.get("Nombre")),
            ("L1", p.get("Fecha_Nacimiento")),
            ("M1", p.get("Edad")),
            ("N1", p.get("Entidad_Nacimiento")),
            ("O1", p.get("Escolaridad")),
            ("P1", p.get("Sexo")),
            ("Q1", p.get("Ocupacion")),
        ]
        
        for celda, valor in actualizaciones:
            sheet.update(celda, [[valor]])
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False
