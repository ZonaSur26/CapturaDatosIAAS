import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def enviar_a_sheets_mapeado(datos_completos):
    try:
        sheet_id = "1hvEq574Hacl2LNkW-vRaqWgkPQ00MaOC2sZ29gm3sME"
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp"], scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1
        
        # 1. Acceso a los bloques de datos
        u = datos_completos.get("Unidad", {})
        p = datos_completos.get("Paciente", {})
        d = datos_completos.get("Deteccion", {}) # Agregué Detección por si lo necesitas
        
        # 2. Construir la lista de valores en el ORDEN EXACTO de tus columnas (A a la Q)
        # Esto asegura que el dato caiga en la columna correcta al hacer append_row
        fila = [
            u.get("Fecha_Captura", ""),     # A
            u.get("Unidad_Notificante", ""),# B
            u.get("Entidad", ""),           # C
            u.get("Municipio", ""),         # D
            u.get("Jurisdiccion", ""),      # E
            u.get("Localidad", ""),         # F
            u.get("CLUES", ""),             # G
            p.get("Expediente", ""),        # H
            p.get("Apellido_Paterno", ""),  # I
            p.get("Apellido_Materno", ""),  # J
            p.get("Nombre", ""),            # K
            p.get("Fecha_Nacimiento", ""),  # L
            p.get("Edad", ""),              # M
            p.get("Entidad_Nacimiento", ""),# N
            p.get("Escolaridad", ""),       # O
            p.get("Sexo", ""),              # P
            p.get("Ocupacion", "")          # Q
        ]
        
        # 3. APPEND_ROW: Añade los datos automáticamente en la primera fila vacía disponible
        sheet.append_row(fila)
            
        return True
    except Exception as e:
        st.error(f"Error al enviar a Google Sheets: {e}")
        return False
