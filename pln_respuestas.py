import random
from gemini_api import responder_gemini

def generar_respuesta(texto):
    saludos = ["hola", "holaaa", "holiii", "holaa", "holi", "buenos días", "buenas tardes", "buenas noches"]
    interes = ["ansiedad", "estrés", "estresado", "abrumado", "triste", "presionado", "preocupado", "tensionado"]

    texto = texto.lower()

    if any(saludo in texto for saludo in saludos):
        saludos_respuesta = [
            "¡Hola! 😊 ¿Cómo te sientes hoy?",
            "¡Holaaa! ¿En qué puedo ayudarte?",
            "¡Holiii! Cuéntame, ¿cómo estás?",
            "¡Hola! Espero que tengas un gran día.",
            "¡Hola! ¿Quieres hablar sobre algo en especial?"
        ]
        comandos = (
            "\n\nEstas son algunas cosas que puedo hacer por ti:\n"
            "• /respiracion - Ejercicio de respiración\n"
            "• /tipsestudio - Consejos para estudiar mejor\n"
            "• /psicologia - Contactar con psicología\n"
            "• /cita - Agendar una cita\n"
            "• /ayuda - Ver todas las opciones disponibles"
            "También puedes escribirme cómo te sientes y veré cómo puedo ayudarte."
        )
        return random.choice(saludos_respuesta) + comandos

    if any(palabra in texto for palabra in interes): 
        return (
            "Entiendo que te sientas así. Es normal experimentar estrés o ansiedad. "
            "¿Te gustaría que te ofrezca un ejercicio de /respiracion, "
            "o quizás algunos /tipsestudio? "
            "Si sientes que necesitas hablar con alguien, puedes consultar el comando /psicologia."
        )

    elif "gracias" in texto:
        return "¡De nada! Estoy aquí para ayudarte cuando lo necesites. 😊"

    # 👉 Si nada coincide, responde usando Gemini
    return responder_gemini(texto)
