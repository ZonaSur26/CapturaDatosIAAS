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
        h = datos_completos.get("Hosp", {})
        ant = datos_completos.get("Antecedentes", {})
        iaas = datos_completos.get("IAAS", {})
        m = datos_completos.get("Micro", {})
        
        # Diccionario auxiliar en caso de que falle la lectura del mes
        meses_ano = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_por_defecto = meses_ano[datetime.now().month - 1]

        # Determinar el mes de destino
        nombre_hoja_mes = u.get("Mes", mes_por_defecto)

        # =======================================================
        # SELECCIÓN O CREACIÓN DINÁMICA DE LA PESTAÑA DEL MES
        # =======================================================
        try:
            sheet = spreadsheet.worksheet(nombre_hoja_mes)
        except gspread.exceptions.WorksheetNotFound:
            hoja_plantilla = spreadsheet.sheet1
            encabezados = hoja_plantilla.row_values(1) 
            
            # Ajustado dinámicamente a las 250 columnas para alojar hasta la 'IH'
            sheet = spreadsheet.add_worksheet(title=nombre_hoja_mes, rows="1000", cols="250")
            
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
                    return valor_fecha 
            if isinstance(valor_fecha, (date, datetime)):
                return valor_fecha.strftime("%d/%m/%Y")
            return ""

        # Procesamos las fechas base
        fecha_nac_formateada = formatear_fecha(p.get("F_Nac"))
        f_ingreso_hosp = formatear_fecha(h.get("F_Ingreso_Hosp"))
        f_ingreso_serv = formatear_fecha(h.get("F_Ingreso_Serv"))
        f_inicio_sint = formatear_fecha(h.get("F_Inicio_Sint"))
        f_deteccion = formatear_fecha(h.get("F_Deteccion"))
        f_resolucion = formatear_fecha(h.get("F_Resolucion"))
        f_egreso_hosp = formatear_fecha(h.get("F_Egreso_Hosp"))
        f_defuncion = formatear_fecha(h.get("F_Defuncion"))
        
        # Fechas microbiológicas
        f_toma_micro = formatear_fecha(m.get("Fecha_Toma"))
        f_res_micro = formatear_fecha(m.get("Fecha_Res"))

        # =======================================================
        # CONSTRUCCIÓN DE LA FILA FINAL MIGRADA (A -> DO)
        # =======================================================
        fila = [
            # --- VENTANA 1: UNIDAD NOTIFICANTE (A - G) ---
            u.get("Fecha", ""),          # A
            u.get("Unidad_Select", ""),  # B
            u.get("Entidad", ""),        # C
            u.get("Municipio", ""),      # D
            u.get("Jurisdicción", ""),   # E
            u.get("Localidad", ""),      # F
            u.get("CLUES", ""),          # G

            # --- VENTANA 2: IDENTIFICACIÓN PACIENTE (H - Z) ---
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

            # --- VENTANA 3: HOSPITALIZACIÓN Y EGRESO (AA - AO) ---
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
            h.get("Folio_Def", ""),            # AO

            # --- VENTANA 4: ANTECEDENTES PERSONALES PATOLÓGICOS (AP - BC) ---
            ant.get("PREMATUREZ", "NO"),                   # AP
            ant.get("BAJO PESO AL NACER", "NO"),            # AQ
            ant.get("DIABETES MELLITUS", "NO"),             # AR
            ant.get("HIPERTENSIÓN ARTERIAL SISTÉMICA", "NO"),  # AS
            ant.get("SOBREPESO", "NO"),                     # AT
            ant.get("OBESIDAD", "NO"),                      # AU
            ant.get("TABAQUISMO", "NO"),                    # AV
            ant.get("DESNUTRICIÓN", "NO"),                  # AW
            ant.get("ENFERMEDAD RENAL CRÓNICA", "NO"),      # AX
            ant.get("EPOC", "NO"),                          # AY
            ant.get("VIH/SIDA", "NO"),                      # AZ
            ant.get("INMUNOSUPRESIÓN", "NO"),               # BA
            ant.get("CANCER", "NO"),                        # BB
            ant.get("OTRO_TEXTO", "NO APLICA"),             # BC

            # --- VENTANA 5: IAAS Y FACTORES DE RIESGO (BD - DA) ---
            iaas.get("Tipo", ""),                           # BD
            iaas.get("Otro", ""),                           # BE
            iaas.get("tipo_deteccion", ""),                 # BF
            iaas.get("Brote", ""),                          # BG
            iaas.get("Folio", ""),                          # BH

            # CIRUGÍAS (BI - CB)
            formatear_fecha(iaas.get("f_cir_1")),          # BI
            iaas.get("grado_1", ""),                        # BJ
            iaas.get("proc_1", ""),                         # BK
            iaas.get("tipo_cir_1", ""),                     # BL
            iaas.get("protesis_1", ""),                     # BM

            formatear_fecha(iaas.get("f_cir_2")),          # BN
            iaas.get("grado_2", ""),                        # BO
            iaas.get("proc_2", ""),                         # BP
            iaas.get("tipo_cir_2", ""),                     # BQ
            iaas.get("protesis_2", ""),                     # BR

            formatear_fecha(iaas.get("f_cir_3")),          # BS
            iaas.get("grado_3", ""),                        # BT
            iaas.get("proc_3", ""),                         # BU
            iaas.get("tipo_cir_3", ""),                     # BV
            iaas.get("protesis_3", ""),                     # BW

            formatear_fecha(iaas.get("f_cir_4")),          # BX
            iaas.get("grado_4", ""),                        # BY
            iaas.get("proc_4", ""),                         # BZ
            iaas.get("tipo_cir_4", ""),                     # CA
            iaas.get("protesis_4", ""),                     # CB

            # RIESGOS NO CONTABILIZABLES (CC - CL)
            iaas.get("nc_1", ""), formatear_fecha(iaas.get("f_nc_1")),  # CC, CD
            iaas.get("nc_2", ""), formatear_fecha(iaas.get("f_nc_2")),  # CE, CF
            iaas.get("nc_3", ""), formatear_fecha(iaas.get("f_nc_3")),  # CG, CH
            iaas.get("nc_4", ""), formatear_fecha(iaas.get("f_nc_4")),  # CI, CJ
            iaas.get("nc_5", ""), formatear_fecha(iaas.get("f_nc_5")),  # CK, CL

            # RIESGOS CONTABILIZABLES (CM - DA)
            iaas.get("c_1", ""), formatear_fecha(iaas.get("f_inst_1")), formatear_fecha(iaas.get("f_ret_1")), # CM, CN, CO
            iaas.get("c_2", ""), formatear_fecha(iaas.get("f_inst_2")), formatear_fecha(iaas.get("f_ret_2")), # CP, CQ, CR
            iaas.get("c_3", ""), formatear_fecha(iaas.get("f_inst_3")), formatear_fecha(iaas.get("f_ret_3")), # CS, CT, CU
            iaas.get("c_4", ""), formatear_fecha(iaas.get("f_inst_4")), formatear_fecha(iaas.get("f_ret_4")), # CV, CW, CX
            iaas.get("c_5", ""), formatear_fecha(iaas.get("f_inst_5")), formatear_fecha(iaas.get("f_ret_5")), # CY, CZ, DA

            # --- VENTANA 6: DIAGNÓSTICO MICROBIOLÓGICO BASE (DB - DO) ---
            m.get("Hemo_ITS", "NO"),    # DB
            m.get("sp", "NO"),          # DC
            m.get("scc", "NO"),         # DD
            m.get("pcc", "NO"),         # DE
            m.get("Tomada", "NO"),      # DF
            f_toma_micro,               # DG
            f_res_micro,                # DH
            m.get("Lab", ""),           # DI
            m.get("Muestra", ""),       # DJ
            m.get("Tecnica", ""),       # DK
            m.get("Resultado", ""),     # DL
            m.get("MicroOrg", ""),      # DM
            m.get("Susp", "NO"),        # DN
            m.get("Prueba_Comp_Resistencia", "NO") # DO
        ]

        # --- SUB-BLOQUE: PANEL DE 62 ANTIBIÓTICOS (DP -> IH) ---
        antibioticos_master = [
            "AMIKACINA", "AMPICILINA", "AMPICILINA-SULBACTAM", "ANFOTERICINA B", "ANIDULAFUNGINA",
            "AZTREONAM", "AZITROMICINA", "CASPOFUNGINA", "CEFAZOLINA", "CEFEDICOL",
            "CEFEPIME", "CEFIXIMA", "CEFOTAXIMA", "CEFOTETAN", "CEFOXITINA",
            "CEFTAROLINA", "CEFTAZIDIMA", "CEFTAZIDIMA-AVIBACTAM", "CEFTOLOZANO-TAZOBACTAM", "CEFTRIAXONA",
            "CEFUROXIMA", "CIPROFLOXACINO", "CLARITROMICINA", "CLINDAMICINA", "CLORANFENICOL",
            "COLISTINA", "DALBAVANCINA", "DAPTOMICINA", "DOXICICLINA", "ERITROMICINA",
            "ERTAPENEM", "ISAVUCONAZOL", "FLUCONAZOL", "FLUCITOSINA", "FOSFOMICINA",
            "GENTAMICINA", "IMIPENEM", "IMIPENEM-RELEBACTAM", "ITRACONAZOL", "LEVOFLOXACINO",
            "LINEZOLID", "MEROPENEM", "MEROPENEM-VABORBACTAM", "METRONIDAZOL", "MICAFUNGINA",
            "MINOCICLINA", "MOXIFLOXACINO", "NITROFURANTOINA", "OXACILINA", "PENICILINA",
            "PIPERACILINA-TAZOBACTAM", "POLIMIXINA B", "POSACONAZOL", "RIFAMPICINA", "TEDIZOLID",
            "TETRACICLINA", "TICARCILINA-CLAVULANATO", "TIGECICLINA", "TOBRAMICINA", "TRIMETOPRIM-SULFAMETOXAZOL",
            "VANCOMICINA", "VORICONAZOL"
        ]

        # Itera ordenadamente de DP (columna 120) hasta IH (columna 243)
        for ab in antibioticos_master:
            fila.append(m.get(f"res_{ab}", "ND"))
            fila.append(m.get(f"cmi_{ab}", ""))

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
