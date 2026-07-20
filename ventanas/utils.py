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
        
        # --- AQUÍ DEFINES TU MAPEO ---
        # Accede a las secciones guardadas en el session_state
        iaas = datos_completos.get("IAAS", {})
        micro = datos_completos.get("Micro", {})
        
        # Lista de actualizaciones (Celda, Valor)
        actualizaciones = [
            ("B2", iaas.get("Tipo")),
            ("B3", iaas.get("tipo_deteccion")),
            ("C5", micro.get("MicroOrg")),
            ("D5", micro.get("Resultado")),
            # Agrega todos los campos que necesites mapear aquí
        ]
        
        # Ejecuta las actualizaciones
        for celda, valor in actualizaciones:
            sheet.update(celda, [[valor]])
            
        return True
    except Exception as e:
        st.error(f"Error al mapear a Sheets: {e}")
        return False
