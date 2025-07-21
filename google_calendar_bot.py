from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Ruta a tu archivo JSON descargado
SERVICE_ACCOUNT_FILE = 'C:/Users/karla/Downloads/gen-lang-client-0838152118-3345c50abd5b.json'

SCOPES = ['https://www.googleapis.com/auth/calendar']

# ID del calendario (usa 'primary' si es tu calendario principal)
CALENDAR_ID = 'primary'

# Autenticación
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

# Función para crear una cita
def crear_cita(nombre, fecha, hora, tema):
    # Convertir fecha y hora a formato RFC3339
    inicio = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    fin = inicio + timedelta(minutes=30)

    evento = {
        'summary': f'Cita con {nombre}',
        'description': f'Tema: {tema}',
        'start': {
            'dateTime': inicio.isoformat(),
            'timeZone': 'America/Mexico_City',
        },
        'end': {
            'dateTime': fin.isoformat(),
            'timeZone': 'America/Mexico_City',
        },
    }

    evento_creado = service.events().insert(calendarId=CALENDAR_ID, body=evento).execute()
    return evento_creado.get('htmlLink')
