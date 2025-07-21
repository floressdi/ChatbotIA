import json
from datetime import datetime, time, date, timedelta
import os
import threading # Necesario para el bloqueo

CITAS_FILE = 'citas.json'
file_lock = threading.Lock() # Objeto de bloqueo para manejar la concurrencia
    
def iniciar_cita():
    if not os.path.exists(CITAS_FILE):
        with open(CITAS_FILE, 'w') as f:
            json.dump({"citas": []}, f, indent=4)

def recibir_citas():
    with file_lock: # Adquirir el bloqueo antes de leer
        with open(CITAS_FILE, 'r') as f:
            return json.load(f)

def guardar_citas(data):
    with file_lock: # Adquirir el bloqueo antes de escribir
        with open(CITAS_FILE, 'w') as f:
            json.dump(data, f, indent=4)

def dia_habil(selected_date_str, selected_time_str):
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        selected_time = datetime.strptime(selected_time_str, '%H:%M').time()

        # 1. Verificar si es un día de semana (Lunes=0 a Viernes=4)
        if not (0 <= selected_date.weekday() <= 4):
            return False, "La fecha debe ser de Lunes a Viernes."

        # 2. Verificar rango de horas (8:00 AM a 3:00 PM como hora de inicio máxima para 1 hora de sesión)
        start_time_limit = time(8, 0)
        end_time_limit_for_booking = time(15, 0) # Última hora de inicio para que la sesión termine a las 4 PM

        if not (start_time_limit <= selected_time <= end_time_limit_for_booking):
            return False, "Las citas son de 8:00 AM a 4:00 PM (la última cita se puede agendar a las 3:00 PM)."

        return True, ""

    except ValueError:
        return False, "Formato de fecha u hora incorrecto. Usa YYYY-MM-DD y HH:MM."

def agendar_cita_json(user_id, username, fecha_str, hora_str):
    is_valid, message =dia_habil(fecha_str, hora_str)
    if not is_valid:
        return False, message

    citas_data = recibir_citas()
    citas = citas_data["citas"]

    # Verificar empalmes
    for cita in citas:
        if cita["fecha"] == fecha_str and cita["hora"] == hora_str:
            return False, f"Lo siento, la hora de las {hora_str} del {fecha_str} ya está ocupada. Por favor, elige otra hora."

    # Si no hay empalmes, agregar la nueva cita
    new_id = len(citas) + 1 # Generar un ID simple (cuidado con IDs en entornos concurrentes)
    new_cita = {
        "id": new_id,
        "user_id": user_id,
        "username": username,
        "fecha": fecha_str,
        "hora": hora_str
    }
    citas.append(new_cita)
    guardar_citas(citas_data) # Guardar los cambios

    return True, "¡Cita agendada con éxito!"

def get_available_times_json(selected_date_str):
    available_slots = []
    # Generar todas las posibles horas de inicio para ese día
    start_time = time(8, 0)
    end_time = time(15, 0) # Última hora de inicio posible
    current_time = datetime.combine(date.today(), start_time)

    while current_time.time() <= end_time:
        available_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(hours=1)

    citas_data = recibir_citas()
    citas = citas_data["citas"]
    
    # Quitar las horas ya ocupadas
    booked_times = [cita["hora"] for cita in citas if cita["fecha"] == selected_date_str]
    
    return [slot for slot in available_slots if slot not in booked_times]



if __name__ == '__main__':
    iniciar_cita()
    # Ejemplos de uso:
    print(agendar_cita_json(123, "alumno_test", "2025-07-28", "09:00"))
    print(agendar_cita_json(124, "otro_alumno", "2025-07-28", "09:00")) # Debería fallar
    print(agendar_cita_json(125, "tercer_alumno", "2025-07-29", "16:00")) # Debería fallar (fuera de rango)
    print(get_available_times_json("2025-07-28"))