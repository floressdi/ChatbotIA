def generar_respuesta(texto):
    texto = texto.lower()

    if "estrés" in texto or "ansiedad" in texto or "abrumado" in texto:
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
