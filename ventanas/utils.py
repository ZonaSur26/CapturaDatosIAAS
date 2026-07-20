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
        h = datos_completos.get("Hosp", {}) # <--- Recuperamos Ventana 3
        
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
            hoja_plantilla = spreadsheet.sheet1
            encabezados = hoja_plantilla.row_values(1) 
            
            # Ampliamos a 45 columnas para dar espacio holgado a futuras ventanas
            sheet = spreadsheet.add_worksheet(title=nombre_hoja_mes, rows="1000", cols="45")
            
            if encabezados:
                sheet.append_row(encabezados)
                
            st.toast(f"ℹ️ Creada nueva pestaña mensual: {nombre_hoja_mes}")

        # =======================================================
        # FUNCIÓN AUXILIAR PARA FORMATEAR FECHAS DE FORMA SEGURA
        # =======================================================
        def formatear_fecha(valor_fecha):
            if not valor_fecha:
                return ""
            if isinstance(valor_fecha, str):
                try:
                    valor_fecha = datetime.strptime(valor_fecha, "%Y-%m-%d").date()
                except ValueError:
                    return valor_fecha # Si ya tiene formato manual, lo conserva
            if isinstance(valor_fecha, (date, datetime)):
                return valor_fecha.strftime("%d/%m/%Y")
            return ""

        # Procesamos todas las fechas
        fecha_nac_formateada = formatear_fecha(p.get("F_Nac"))
        f_ingreso_hosp = formatear_fecha(h.get("F_Ingreso_Hosp"))
        f_ingreso_serv = formatear_fecha(h.get("F_Ingreso_Serv"))
        f_inicio_sint = formatear_fecha(h.get("F_Inicio_Sint"))
        f_deteccion = formatear_fecha(h.get("F_Deteccion"))
        f_resolucion = formatear_fecha(h.get("F_Resolucion"))
        f_egreso_hosp = formatear_fecha(h.get("F_Egreso_Hosp"))
        f_defuncion = formatear_fecha(h.get("F_Defuncion"))

        # =======================================================
        # CONSTRUCCIÓN DE LA FILA FINAL MIGRADA (A -> AO)
        # =======================================================
        fila = [
            # --- VENTANA 1: UNIDAD NOTIFICANTE ---
            u.get("Fecha", ""),          # A
            u.get("Unidad_Select", ""),  # B
            u.get("Entidad", ""),        # C
            u.get("Municipio", ""),      # D
            u.get("Jurisdicción", ""),   # E
            u.get("Localidad", ""),      # F
            u.get("CLUES", ""),          # G

            # --- VENTANA 2: IDENTIFICACIÓN PACIENTE ---
            p.get("Expediente", ""),     # H
            p.get("Ap_Paterno", ""),     # I
            p.get("Ap_Materno", ""),     # J
            p.get("Nombres", ""),        # K
            fecha_nac_formateada,        # L
            p.get("Edad", ""),           # M
            p.get("Entidad_Nac", ""),    # N
            p.get("Escolaridad", ""),    # O
            p.get("Sexo", ""),           # P
            p.get("Ocupacion", ""),      # Q
            p.get("Indigena", ""),       # R
            p.get("Habla_Lengua", ""),   # S
            p.get("Es_Migrante", ""),    # T
            p.get("Nacionalidad", ""),   # U
            p.get("Origen", ""),         # V
            p.get("T1", ""),             # W
            p.get("T2", ""),             # X
            p.get("T3", ""),             # Y
            p.get("T4", ""),             # Z

            # --- VENTANA 3: HOSPITALIZACIÓN Y EGRESO ---
            h.get("Tipo_Ingreso", ""),         # AA
            h.get("Tipo_Servicio", ""),        # AB
            h.get("Cama", ""),                 # AC
            h.get("Servicio_IAAS", ""),        # AD
            h.get("Diagnostico_Ingreso", ""),  # AE
            f_ingreso_hosp,                    # AF
            f_ingreso_serv,                    # AG
            f_inicio_sint,                     # AH
            f_deteccion,                       # AI
            f_resolucion,                      # AJ
            f_egreso_hosp,                     # AK
            h.get("Motivo_Egreso", ""),        # AL
            f_defuncion,                       # AM
            h.get("Causa_Muerte", ""),         # AN
            h.get("Folio_Def", "")             # AO
            ant.get("PREMATUREZ", "NO"),                  # AP
    ant.get("BAJO PESO AL NACER", "NO"),           # AQ
    ant.get("DIABETES MELLITUS", "NO"),            # AR
    ant.get("HIPERTENSIÓN ARTERIAL SISTÉMICA", "NO"), # AS
    ant.get("SOBREPESO", "NO"),                    # AT
    ant.get("OBESIDAD", "NO"),                     # AU
    ant.get("TABAQUISMO", "NO"),                   # AV
    ant.get("DESNUTRICIÓN", "NO"),                 # AW
    ant.get("ENFERMEDAD RENAL CRÓNICA", "NO"),     # AX
    ant.get("EPOC", "NO"),                         # AY
    ant.get("VIH/SIDA", "NO"),                     # AZ
    ant.get("INMUNOSUPRESIÓN", "NO"),              # BA
    ant.get("CANCER", "NO"),                       # BB
    ant.get("OTRO_TEXTO", "NO APLICA")             # BC -> Si se seleccionó, entra el texto; si no, "NO APLICA"
])
        

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
