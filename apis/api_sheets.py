import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def update_sheets(data_update_sheets, planilha, id_planilha):
  creds = None
  if os.path.exists("token.json"):
    try:
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
      if creds and not creds.expired and creds.refresh_token:
        try:
          creds.refresh(Request())
        except google.auth.exceptions.RefreshError:
          print("Token expirado ou revogado. Deletando token.")
          os.remove(token_path)
          return update_sheets(data_update_sheets, planilha, id_planilha)
        if creds.expired and creds.refresh_token:
          creds.refresh(Request())

    except (google.auth.exceptions.GoogleAuthError, ValueError):
      print("Erro ao carregar o token. Deletando token.")
      os.remove("token.json")
      return update_sheets(data_update_sheets, planilha, id_planilha)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "client_secret.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
    
  service = build("sheets", "v4", credentials=creds)

  # Call the Sheets API
  sheet = service.spreadsheets()
  result = sheet.values().update(spreadsheetId=id_planilha, 
                                  range=planilha, valueInputOption="USER_ENTERED",
                                  body={"values": data_update_sheets}).execute()
  return data_update_sheets

def local_Sheets(planilha, id_planilha):
    creds = None
    token_path = "token.json"

    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print("⚠️ Token expirado ou revogado. Deletando token.")
                    os.remove(token_path)
                    return local_Sheets(planilha, id_planilha)
        except Exception as e:
            print("⚠️ Erro ao carregar o token. Deletando token.")
            os.remove(token_path)
            return local_Sheets(planilha, id_planilha)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=id_planilha, range=planilha).execute()
    values = result.get("values", [])
    return values
