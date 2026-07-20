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
        poli = datos_completos.get("Polimicrobiana", {})
        tx = datos_completos.get("Tratamiento", {})
        det = datos_completos.get("Deteccion", {})
        
        # Determinación del mes de destino
        meses_ano = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_por_defecto = meses_ano[datetime.now().month - 1]
        
        # Aseguramos que el nombre esté limpio de espacios accidentales
        nombre_hoja_target = str(u.get("Mes", mes_por_defecto)).strip().capitalize()

        # =======================================================
        # BÚSQUEDA DIRECTA Y CREACIÓN DE PESTAÑA SIN DUPLICAR
        # =======================================================
        try:
            # Intenta abrir la hoja del mes directamente
            sheet = spreadsheet.worksheet(nombre_hoja_target)
        except gspread.exceptions.WorksheetNotFound:
            # Si NO existe, la crea dinámicamente con 400 columnas
            sheet = spreadsheet.add_worksheet(title=nombre_hoja_target, rows="1000", cols="400")
            st.toast(f"ℹ️ Creada nueva pestaña mensual: {nombre_hoja_target}")

        # =======================================================
        # CONSTRUCCIÓN MAESTRA DE LOS 396 ENCABEZADOS (FILA 1)
        # =======================================================
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

        encabezados_396 = [
            # V1: UNIDAD (A - G)
            "FECHA DE NOTIFICACIÓN", "NOMBRE DE LA UNIDAD", "ENTIDAD FEDERATIVA", "MUNICIPIO", "JURISDICCIÓN SANITARIA", "LOCALIDAD", "CLUES",
            # V2: PACIENTE (H - Z)
            "NÚMERO DE EXPEDIENTE", "APELLIDO PATERNO", "APELLIDO MATERNO", "NOMBRE(S)", "FECHA DE NACIMIENTO", "EDAD", "ENTIDAD DE NACIMIENTO", 
            "ESCOLARIDAD", "SEXO", "OCUPACIÓN", "PERTENECE A POBLACIÓN INDÍGENA", "HABLA LENGUA INDÍGENA", "CONDICIÓN DE MIGRANTE", "NACIONALIDAD", 
            "LUGAR DE ORIGEN", "PAÍS DE TRÁNSITO 1", "PAÍS DE TRÁNSITO 2", "PAÍS DE TRÁNSITO 3", "PAÍS DE TRÁNSITO 4",
            # V3: HOSPITALIZACIÓN (AA - AO)
            "TIPO DE INGRESO", "TIPO DE SERVICIO", "NÚMERO DE CAMA", "SERVICIO DONDE SE ADQUIRIÓ LA IAAS", "DIAGNÓSTICO DE INGRESO (CIE-10)", 
            "FECHA DE INGRESO HOSPITALARIO", "FECHA DE INGRESO AL SERVICIO", "FECHA DE INICIO DE SÍNTOMAS DE IAAS", "FECHA DE DETECCIÓN DE IAAS", 
            "FECHA DE RESOLUCIÓN DE IAAS", "FECHA DE EGRESO HOSPITALARIO", "MOTIVO DE EGRESO", "FECHA DE DEFUNCIÓN", "CAUSA DE MUERTE", "FOLIO DE CERTIFICADO DE DEFUNCIÓN",
            # V4: ANTECEDENTES (AP - BC)
            "ANTECEDENTE: PREMATUREZ", "ANTECEDENTE: BAJO PESO AL NACER", "ANTECEDENTE: DIABETES MELLITUS", "ANTECEDENTE: HIPERTENSIÓN ARTERIAL SISTÉMICA", 
            "ANTECEDENTE: SOBREPESO", "ANTECEDENTE: OBESIDAD", "ANTECEDENTE: TABAQUISMO", "ANTECEDENTE: DESNUTRICIÓN", "ANTECEDENTE: ENFERMEDAD RENAL CRÓNICA", 
            "ANTECEDENTE: EPOC", "ANTECEDENTE: VIH/SIDA", "ANTECEDENTE: INMUNOSUPRESIÓN", "ANTECEDENTE: CÁNCER", "OTRO ANTECEDENTE (ESPECIFIQUE)",
            # V5: IAAS Y RIESGOS (BD - DA)
            "TIPO DE IAAS", "ESPECIFIQUE OTRA IAAS", "TIPO DE DETECCIÓN DE IAAS", "IAAS ASOCIADA A BROTE", "FOLIO DE BROTE",
            "FECHA CIRUGÍA 1", "GRADO DE CONTAMINACIÓN CIRUGÍA 1", "PROCEDIMIENTO QUIRÚRGICO 1", "TIPO DE CIRUGÍA 1", "PRÓTESIS / IMPLANTE EN CIRUGÍA 1",
            "FECHA CIRUGÍA 2", "GRADO DE CONTAMINACIÓN CIRUGÍA 2", "PROCEDIMIENTO QUIRÚRGICO 2", "TIPO DE CIRUGÍA 2", "PRÓTESIS / IMPLANTE EN CIRUGÍA 2",
            "FECHA CIRUGÍA 3", "GRADO DE CONTAMINACIÓN CIRUGÍA 3", "PROCEDIMIENTO QUIRÚRGICO 3", "TIPO DE CIRUGÍA 3", "PRÓTESIS / IMPLANTE EN CIRUGÍA 3",
            "FECHA CIRUGÍA 4", "GRADO DE CONTAMINACIÓN CIRUGÍA 4", "PROCEDIMIENTO QUIRÚRGICO 4", "TIPO DE CIRUGÍA 4", "PRÓTESIS / IMPLANTE EN CIRUGÍA 4",
            "RIESGO NO CONTABILIZABLE 1", "FECHA RIESGO NO CONTABILIZABLE 1", "RIESGO NO CONTABILIZABLE 2", "FECHA RIESGO NO CONTABILIZABLE 2",
            "RIESGO NO CONTABILIZABLE 3", "FECHA RIESGO NO CONTABILIZABLE 3", "RIESGO NO CONTABILIZABLE 4", "FECHA RIESGO NO CONTABILIZABLE 4",
            "RIESGO NO CONTABILIZABLE 5", "FECHA RIESGO NO CONTABILIZABLE 5",
            "RIESGO CONTABILIZABLE 1", "FECHA INSTALACIÓN RIESGO 1", "FECHA RETIRO RIESGO 1",
            "RIESGO CONTABILIZABLE 2", "FECHA INSTALACIÓN RIESGO 2", "FECHA RETIRO RIESGO 2",
            "RIESGO CONTABILIZABLE 3", "FECHA INSTALACIÓN RIESGO 3", "FECHA RETIRO RIESGO 3",
            "RIESGO CONTABILIZABLE 4", "FECHA INSTALACIÓN RIESGO 4", "FECHA RETIRO RIESGO 4",
            "RIESGO CONTABILIZABLE 5", "FECHA INSTALACIÓN RIESGO 5", "FECHA RETIRO RIESGO 5",
            # V6: MICROBIOLOGÍA BASE (DB - DP)
            "HEMOCULTIVOS PARA ITS", "SANGRE PERIFÉRICA", "SANGRE POR CATÉTER CENTRAL", "PUNTA DE CATÉTER CENTRAL", "¿SE TOMÓ MUESTRA MICROBIOLÓGICA?", 
            "FECHA DE TOMA DE MUESTRA", "FECHA DE RESULTADO MICROBIOLÓGICO", "LABORATORIO QUE PROCESÓ", "TIPO DE MUESTRA", "TÉCNICA DE DIAGNÓSTICO MICROBIOLÓGICO", 
            "RESULTADO DEL CULTIVO", "MICROORGANISMO AISLADO", "ESPECIFIQUE OTRO MICROORGANISMO", "¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD?", "TÉCNICA DE SUSCEPTIBILIDAD ANTIMICROBIANA"
        ]

        # V6: PANEL ATB 1 (DQ - IJ)
        for ab in antibioticos_master:
            encabezados_396.append(f"{ab} (INTERPRETACIÓN)")
            encabezados_396.append(f"{ab} (CMI)")

        # V7: POLIMICROBIANA BASE (IK - IO)
        encabezados_396.extend([
            "¿ES INFECCIÓN POLIMICROBIANA?", "POLI - MICROORGANISMO ADICIONAL", "POLI - ESPECIFIQUE OTRO MICROORGANISMO", 
            "POLI - ¿SE REALIZÓ PRUEBA DE SUSCEPTIBILIDAD?", "POLI - TÉCNICA DE SUSCEPTIBILIDAD"
        ])

        # V7: PANEL ATB 2 (IP - NI)
        for ab in antibioticos_master:
            encabezados_396.append(f"POLI - {ab} (INTERPRETACIÓN)")
            encabezados_396.append(f"POLI - {ab} (CMI)")

        # V8: TRATAMIENTO (NJ - NX)
        for i in range(1, 6):
            encabezados_396.append(f"TRATAMIENTO {i} - ANTIMICROBIANO")
            encabezados_396.append(f"TRATAMIENTO {i} - FECHA INICIO")
            encabezados_396.append(f"TRATAMIENTO {i} - FECHA TÉRMINO")

        # V9: DETECCIÓN (NY - OF)
        encabezados_396.extend([
            "PERSONAL QUE NOTIFICA", "ESPECIFIQUE OTRO PERSONAL QUE NOTIFICA", "RESPONSABLE DE LA DETECCIÓN", 
            "RESPONSABLE DE LA CAPTURA", "RESPONSABLE DE LA UVEH", "¿LA IAAS FUE ADQUIRIDA EN OTRA UNIDAD?", 
            "NOMBRE DE LA OTRA UNIDAD", "ESTADO DE LA OTRA UNIDAD"
        ])

        # VERIFICACIÓN Y FORMATO DE ENCABEZADOS EN LA FILA 1
        fila_1_actual = sheet.row_values(1)
        if not fila_1_actual:
            sheet.append_row(encabezados_396)
            sheet.format('1:1', {
                "textFormat": {"bold": True, "fontSize": 10},
                "backgroundColor": {"red": 1.0, "green": 0.95, "blue": 0.7},
                "horizontalAlignment": "CENTER"
            })

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
        
        f_toma_micro = formatear_fecha(m.get("Fecha_Toma"))
        f_res_micro = formatear_fecha(m.get("Fecha_Res"))

        # =======================================================
        # CONSTRUCCIÓN DE LA FILA DE DATOS DEL PACIENTE (A -> OF)
        # =======================================================
        fila = [
            # VENTANA 1
            u.get("Fecha", ""), u.get("Unidad_Select", ""), u.get("Entidad", ""), u.get("Municipio", ""), u.get("Jurisdicción", ""), u.get("Localidad", ""), u.get("CLUES", ""),
            # VENTANA 2
            p.get("Expediente", ""), p.get("Ap_Paterno", ""), p.get("Ap_Materno", ""), p.get("Nombres", ""), fecha_nac_formateada, p.get("Edad", ""), p.get("Entidad_Nac", ""), 
            p.get("Escolaridad", ""), p.get("Sexo", ""), p.get("Ocupacion", ""), p.get("Indigena", ""), p.get("Habla_Lengua", ""), p.get("Es_Migrante", ""), p.get("Nacionalidad", ""), 
            p.get("Origen", ""), p.get("T1", ""), p.get("T2", ""), p.get("T3", ""), p.get("T4", ""),
            # VENTANA 3
            h.get("Tipo_Ingreso", ""), h.get("Tipo_Servicio", ""), h.get("Cama", ""), h.get("Servicio_IAAS", ""), h.get("Diagnostico_Ingreso", ""), f_ingreso_hosp, f_ingreso_serv, 
            f_inicio_sint, f_deteccion, f_resolucion, f_egreso_hosp, h.get("Motivo_Egreso", ""), f_defuncion, h.get("Causa_Muerte", ""), h.get("Folio_Def", ""),
            # VENTANA 4
            ant.get("PREMATUREZ", "NO"), ant.get("BAJO PESO AL NACER", "NO"), ant.get("DIABETES MELLITUS", "NO"), ant.get("HIPERTENSIÓN ARTERIAL SISTÉMICA", "NO"), 
            ant.get("SOBREPESO", "NO"), ant.get("OBESIDAD", "NO"), ant.get("TABAQUISMO", "NO"), ant.get("DESNUTRICIÓN", "NO"), ant.get("ENFERMEDAD RENAL CRÓNICA", "NO"), 
            ant.get("EPOC", "NO"), ant.get("VIH/SIDA", "NO"), ant.get("INMUNOSUPRESIÓN", "NO"), ant.get("CANCER", "NO"), ant.get("OTRO_TEXTO", "NO APLICA"),
            # VENTANA 5
            iaas.get("Tipo", ""), iaas.get("Otro", ""), iaas.get("tipo_deteccion", ""), iaas.get("Brote", ""), iaas.get("Folio", ""),
            formatear_fecha(iaas.get("f_cir_1")), iaas.get("grado_1", ""), iaas.get("proc_1", ""), iaas.get("tipo_cir_1", ""), iaas.get("protesis_1", ""),
            formatear_fecha(iaas.get("f_cir_2")), iaas.get("grado_2", ""), iaas.get("proc_2", ""), iaas.get("tipo_cir_2", ""), iaas.get("protesis_2", ""),
            formatear_fecha(iaas.get("f_cir_3")), iaas.get("grado_3", ""), iaas.get("proc_3", ""), iaas.get("tipo_cir_3", ""), iaas.get("protesis_3", ""),
            formatear_fecha(iaas.get("f_cir_4")), iaas.get("grado_4", ""), iaas.get("proc_4", ""), iaas.get("tipo_cir_4", ""), iaas.get("protesis_4", ""),
            iaas.get("nc_1", ""), formatear_fecha(iaas.get("f_nc_1")), iaas.get("nc_2", ""), formatear_fecha(iaas.get("f_nc_2")),
            iaas.get("nc_3", ""), formatear_fecha(iaas.get("f_nc_3")), iaas.get("nc_4", ""), formatear_fecha(iaas.get("f_nc_4")),
            iaas.get("nc_5", ""), formatear_fecha(iaas.get("f_nc_5")),
            iaas.get("c_1", ""), formatear_fecha(iaas.get("f_inst_1")), formatear_fecha(iaas.get("f_ret_1")),
            iaas.get("c_2", ""), formatear_fecha(iaas.get("f_inst_2")), formatear_fecha(iaas.get("f_ret_2")),
            iaas.get("c_3", ""), formatear_fecha(iaas.get("f_inst_3")), formatear_fecha(iaas.get("f_ret_3")),
            iaas.get("c_4", ""), formatear_fecha(iaas.get("f_inst_4")), formatear_fecha(iaas.get("f_ret_4")),
            iaas.get("c_5", ""), formatear_fecha(iaas.get("f_inst_5")), formatear_fecha(iaas.get("f_ret_5")),
            # VENTANA 6 BASE
            m.get("Hemo_ITS", "NO"), m.get("sp", "NO"), m.get("scc", "NO"), m.get("pcc", "NO"), m.get("Tomada", "NO"), 
            f_toma_micro, f_res_micro, m.get("Lab", ""), m.get("Muestra", ""), m.get("Tecnica", ""), m.get("Resultado", ""), 
            m.get("MicroOrg", ""), m.get("Otro_MicroOrg", ""), m.get("Susp", "NO"), m.get("Tecnica_Susp", "")
        ]

        # VENTANA 6 ATB
        for ab in antibioticos_master:
            fila.append(m.get(f"res_{ab}", "ND"))
            fila.append(m.get(f"cmi_{ab}", ""))

        # VENTANA 7 BASE
        fila.extend([
            poli.get("Es_Polimicrobiana", "NO"), poli.get("MicroOrg", ""), poli.get("Otro_MicroOrg", ""), 
            poli.get("Susp", "NO"), poli.get("Tecnica_Susp", "")
        ])

        # VENTANA 7 ATB
        for ab in antibioticos_master:
            fila.append(poli.get(f"poli_res_{ab}", "ND"))
            fila.append(poli.get(f"poli_cmi_{ab}", ""))

        # VENTANA 8
        for i in range(1, 6):
            f_tx = tx.get(f"Fila_{i}", {})
            fila.append(f_tx.get("AB", ""))
            fila.append(formatear_fecha(f_tx.get("Inicio")))
            fila.append(formatear_fecha(f_tx.get("Fin")))

        # VENTANA 9
        fila.extend([
            det.get("Personal_Notifica", ""), det.get("Espec_Otro", ""), det.get("Resp_Deteccion", ""), 
            det.get("Resp_Captura", ""), det.get("Resp_UVEH", ""), det.get("Otra_Unidad", "NO"), 
            det.get("Nombre_Unidad", ""), det.get("Estado_Unidad", "")
        ])

        # Inserción limpia en Google Sheets
        sheet.append_row(fila, value_input_option="USER_ENTERED")
        return True

    except Exception as e:
        st.error("Error crítico en la comunicación con Google Sheets.")
        st.exception(e)
        return False
