import random

def generar_respuesta(texto):
    saludos = ["hola", "holaaa", "holiii", "holaa", "holi", "buenos días", "buenas tardes", "buenas noches"]
    interes =["ansiedad", "estrés", "estresado", "abrumado", "triste", "Presionado", "Preocupado", "Tensionado"]

    texto = texto.lower()

    if any(saludo in texto for saludo in saludos):
        respuesta =[
            "¡Hola! 😊 ¿Cómo te sientes hoy?",
            "¡Holaaa! ¿En qué puedo ayudarte?",
            "¡Holiii! Cuéntame, ¿cómo estás?",
            "¡Hola! Espero que tengas un gran día.",
            "¡Hola! ¿Quieres hablar sobre algo en especial?"
        ]
        return random.choice(respuesta)


    if any(palabra in texto for palabra in interes ): 
        return (
            "Entiendo que te sientas así. Es normal experimentar estrés o ansiedad. "
            "¿Te gustaría que te ofrezca un ejercicio de /respiracion, "
            "o quizás algunos /tipsestudio? "
            "Si sientes que necesitas hablar con alguien, puedes consultar el comando /psicologia."
        )
    elif "gracias" in texto:
        return "¡De nada! Estoy aquí para ayudarte cuando lo necesites. 😊"
    else:
        return (
            "Lo siento, no estoy seguro de cómo ayudarte con eso. "
            "Puedes usar /ayuda para ver las opciones que tengo disponibles."
        )
