import google.generativeai as genai

genai.configure(api_key="AIzaSyBhw6fPRAnQF3361PJb9FYjiEMpYPe68V8")

model = genai.GenerativeModel("models/gemini-1.5-flash")

def responder_gemini(prompt_usuario):
    try:
        prompt_sistema = (
            "Responde como un asistente experto en el manejo del estrés y la ansiedad en estudiantes. "
            "Solo puedes hablar sobre estos temas. Si el usuario pregunta algo fuera de ese contexto, "
            "responde amablemente que solo puedes ayudar con temas relacionados a la ansiedad o el estrés académico.\n\n"
            f"Usuario: {prompt_usuario}"
        )
        response = model.generate_content(prompt_sistema)
        return response.text
    except Exception as e:
        if "quota" in str(e).lower():
            return "😓 He alcanzado el límite de uso diario. Intenta más tarde."
        return "Lo siento, no pude generar una respuesta en este momento."
