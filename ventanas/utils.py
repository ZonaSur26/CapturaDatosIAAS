import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
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

        sheet = client.open_by_key(SHEET_ID).sheet1

        u = datos_completos.get("Unidad", {})
        p = datos_completos.get("Paciente", {})

        # ==========================
        # CALCULAR EDAD
        # ==========================

        edad = ""

        if p.get("F_Nac"):

            delta = relativedelta(date.today(), p["F_Nac"])

            edad = f"{delta.years} Años {delta.months} Meses {delta.days} Días"

        # ==========================
        # FILA
        # ==========================

        fila = [

            # A
            u.get("Fecha", ""),

            # B
            u.get("Unidad_Select", ""),

            # C
            u.get("Entidad", ""),

            # D
            u.get("Municipio", ""),

            # E
            u.get("Jurisdicción", ""),

            # F
            u.get("Localidad", ""),

            # G
            u.get("CLUES", ""),

            # H
            p.get("Expediente", ""),

            # I
            p.get("Ap_Paterno", ""),

            # J
            p.get("Ap_Materno", ""),

            # K
            p.get("Nombres", ""),

            # L
            p.get("F_Nac", "").strftime("%d/%m/%Y") if p.get("F_Nac") else "",

            # M
            edad,

            # N
            p.get("Entidad_Nac", ""),

            # O
            p.get("Escolaridad", ""),

            # P
            p.get("Sexo", ""),

            # Q
            p.get("Ocupacion", ""),
        ]

        sheet.append_row(
            fila,
            value_input_option="USER_ENTERED",
        )

        return True

    except Exception as e:

        st.exception(e)

        return False
