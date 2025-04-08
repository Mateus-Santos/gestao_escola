import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_valid_credentials(scopes, token_path="token.json", client_secret_path="client_secret.json"):
    creds = None

    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, scopes)
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    print("⚠️ Token expirado ou revogado. Deletando token.")
                    os.remove(token_path)
                    return get_valid_credentials(scopes, token_path, client_secret_path)
        except Exception:
            print("⚠️ Erro ao carregar o token. Deletando token.")
            os.remove(token_path)
            return get_valid_credentials(scopes, token_path, client_secret_path)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes)
        creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return creds

def update_sheets(data_update_sheets, planilha, id_planilha):
    creds = get_valid_credentials(SCOPES)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    sheet.values().update(
        spreadsheetId=id_planilha,
        range=planilha,
        valueInputOption="USER_ENTERED",
        body={"values": data_update_sheets}
    ).execute()
    return data_update_sheets

def local_Sheets(planilha, id_planilha):
    creds = get_valid_credentials(SCOPES)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=id_planilha, range=planilha).execute()
    return result.get("values", [])