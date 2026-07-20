import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, datetime

def enviar_a_sheets_mapeado(datos_completos):
    try:
        # ID de tu Google Sheets configurado
        SHEET_ID = "1hvEq574Hacl2LNkW-vRaqWgkPQ00MaOC2sZ29gm3sME"
        
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        # Autenticación segura mediante los Secrets de Streamlit
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            st.secrets["gcp"],
            scope,
        )

        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SHEET_ID)
        
        # Recuperamos los sub-diccionarios de la memoria global
        u = datos_completos.get("Unidad", {})
        p = datos_completos.get("Paciente", {})
        
        # Diccionario auxiliar en caso de que falle la lectura del mes
        meses_ano = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_por_defecto = meses_ano[datetime.now().month - 1]

        # Determinar el mes de destino (si no viene, usa el mes en curso en español)
        nombre_hoja_mes = u.get("Mes", mes_por_defecto)

        # =======================================================
        # SELECCIÓN O CREACIÓN DINÁMICA DE LA PESTAÑA DEL MES
        # =======================================================
        try:
            sheet = spreadsheet.worksheet(nombre_hoja_mes)
        except gspread.exceptions.WorksheetNotFound:
            # Si la pestaña no existe, leemos la fila 1 de la hoja principal como plantilla
            hoja_plantilla = spreadsheet.sheet1
            encabezados = hoja_plantilla.row_values(1) 
            
            # Creamos la pestaña nueva con soporte para las 30 columnas
            sheet = spreadsheet.add_worksheet(title=nombre_hoja_mes, rows="1000", cols="30")
            
            # Le asignamos la misma cabecera
            if encabezados:
                sheet.append_row(encabezados)
                
            st.toast(f"ℹ️ Creada nueva pestaña mensual: {nombre_hoja_mes}")

        # ==========================================
        # FORMATO DE FECHA DE NACIMIENTO
        # ==========================================
        fecha_nac_formateada = ""
        f_nac = p.get("F_Nac")

        if f_nac:
            # Validamos si viene como string (por seguridad) o como objeto date directo
            if isinstance(f_nac, str):
                try:
                    f_nac = datetime.strptime(f_nac, "%Y-%m-%d").date()
                except ValueError:
                    f_nac = None

            if isinstance(f_nac, (date, datetime)):
                fecha_nac_formateada = f_nac.strftime("%d/%m/%Y")

        # ==========================================
        # CONSTRUCCIÓN DE LA FILA FINAL MIGRADA
        # ==========================================
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
            p.get("Edad", ""),           # M <--- Recibe el formato inteligente (Años/Meses/Días)
            p.get("Entidad_Nac", ""),    # N
            p.get("Escolaridad", ""),    # O
            p.get("Sexo", ""),           # P
            p.get("Ocupacion", ""),      # Q
            
            # Nuevos campos agregados respetando las letras
            p.get("Indigena", ""),       # R -> ¿Se reconoce como indígena?
            p.get("Habla_Lengua", ""),   # S -> ¿Habla alguna lengua indígena?
            p.get("Es_Migrante", ""),    # T -> ¿El paciente es migrante?
            p.get("Nacionalidad", ""),   # U -> País de nacionalidad
            p.get("Origen", ""),         # V -> País de origen
            p.get("T1", ""),             # W -> País de tránsito 1
            p.get("T2", ""),             # X -> País de tránsito 2
            p.get("T3", ""),             # Y -> País de tránsito 3
            p.get("T4", "")              # Z -> País de tránsito 4
        ]

        # Inserción limpia en Google Sheets
        sheet.append_row(
            fila,
            value_input_option="USER_ENTERED",
        )

        return True

    except Exception as e:
        st.error("Error crítico en la comunicación con Google Sheets.")
        st.exception(e)
        return False
