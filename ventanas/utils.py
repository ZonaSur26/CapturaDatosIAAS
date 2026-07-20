import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def enviar_a_sheets_mapeado(datos_completos):
    try:
        SHEET_ID = "1hvEq574Hacl2LNkW-vRaqWgkPQ00MaOC2sZ29gm3sME"
        
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            st.secrets["gcp"],
            scope,
        )

        client = gspread.authorize(creds)
        
        # 1. Abrimos el libro de Google Sheets
        spreadsheet = client.open_by_key(SHEET_ID)
        
        # 2. Obtener el mes seleccionado desde el formulario
        u = datos_completos.get("Unidad", {})
        p = datos_completos.get("Paciente", {})
        
        # Si por alguna razón no viene el mes, usamos el mes actual por defecto
        nombre_hoja_mes = u.get("Mes", datetime.now().strftime("%B").capitalize())

        # =======================================================
        # LÓGICA DE SELECCIÓN / CREACIÓN DE LA HOJA DEL MES
        # =======================================================
        try:
            # Intentamos abrir la hoja del mes seleccionado (ej. "Junio")
            sheet = spreadsheet.worksheet(nombre_hoja_mes)
        except gspread.exceptions.WorksheetNotFound:
            # SI NO EXISTE: La creamos dinámicamente
            # Tomamos la primera hoja (sheet1) como plantilla para copiar los encabezados (Fila 1)
            hoja_plantilla = spreadsheet.sheet1
            encabezados = hoja_plantilla.row_values(1) 
            
            # Creamos la nueva hoja con el nombre del mes
            sheet = spreadsheet.add_worksheet(title=nombre_hoja_mes, rows="1000", cols="20")
            
            # Le insertamos los mismos encabezados en la primera fila para que mantenga el formato
            if encabezados:
                sheet.append_row(encabezados)
                
            st.toast(f"ℹ️ Se ha creado la nueva pestaña para el mes de: {nombre_hoja_mes}")

        # ==========================================
        # PROCESAR Y VALIDAR FECHA DE NACIMIENTO
        # ==========================================
        edad = ""
        fecha_nac_formateada = ""
        f_nac = p.get("F_Nac")

        if f_nac:
            if isinstance(f_nac, str):
                try:
                    f_nac = datetime.strptime(f_nac, "%Y-%m-%d").date()
                except ValueError:
                    f_nac = None

            if isinstance(f_nac, (date, datetime)):
                delta = relativedelta(date.today(), f_nac)
                edad = f"{delta.years} Años {delta.months} Meses {delta.days} Días"
                fecha_nac_formateada = f_nac.strftime("%d/%m/%Y")

        # ==========================
        # ARMADO DE LA FILA
        # ==========================
        fila = [
            u.get("Fecha", ""),          # A
            u.get("Unidad_Select", ""),  # B
            u.get("Entidad", ""),        # C
            u.get("Municipio", ""),      # D
            u.get("Jurisdicción", ""),   # E
            u.get("Localidad", ""),      # F
            u.get("CLUES", ""),          # G
            p.get("Expediente", ""),     # H
            p.get("Ap_Paterno", ""),     # I
            p.get("Ap_Materno", ""),     # J
            p.get("Nombres", ""),        # K
            fecha_nac_formateada,        # L
            edad,                        # M
            p.get("Entidad_Nac", ""),    # N
            p.get("Escolaridad", ""),    # O
            p.get("Sexo", ""),           # P
            p.get("Ocupacion", "")       # Q
        ]

        # 3. Guardamos la fila en la hoja que corresponda (ya sea la existente o la recién creada)
        sheet.append_row(
            fila,
            value_input_option="USER_ENTERED",
        )

        return True

    except Exception as e:
        st.error("Error al enviar datos a Google Sheets")
        st.exception(e)
        return False
