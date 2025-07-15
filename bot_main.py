import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# --- 1. Configuración Inicial ---
# Configura el log para ver lo que hace tu bot (opcional pero muy útil para depurar)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Reemplaza 'TU_BOT_TOKEN' con el token que obtuviste de BotFather
BOT_TOKEN = "TU_BOT_TOKEN"

# --- 2. Funciones de Manejo de Comandos y Mensajes ---

# Comando /start: Saludo inicial y bienvenida
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"¡Hola, {user.mention_html()}! 👋 Soy tu compañero de salud mental en la universidad. "
        "Estoy aquí para ayudarte si te sientes estresado o ansioso. "
        "Puedes preguntarme sobre técnicas de relajación, o si lo necesitas, "
        "conectarte con el departamento de psicología. "
        "Usa /ayuda para ver qué más puedo hacer por ti."
    )

# Comando /ayuda: Muestra las opciones disponibles
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Aquí tienes algunas cosas que puedo hacer:\n"
        "/respiracion - Te guío en un ejercicio de respiración.\n"
        "/tipsestudio - Consejos para manejar el estrés académico.\n"
        "/psicologia - Información para contactar al departamento de psicología.\n"
        "También puedes escribirme cómo te sientes y veré cómo puedo ayudarte."
    )

# Comando /respiracion: Guía un ejercicio de respiración
async def respiracion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "¡Claro! Vamos a hacer un ejercicio de respiración profunda. 🧘‍♀️\n"
        "1. Inhala lentamente por la nariz contando hasta 4.\n"
        "2. Sostén la respiración contando hasta 7.\n"
        "3. Exhala lentamente por la boca contando hasta 8.\n"
        "Repite esto 3-5 veces. Concéntrate solo en tu respiración."
    )

# Comando /tipsestudio: Ofrece consejos para el estrés académico
async def tips_estudio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Aquí tienes algunos tips para manejar el estrés académico: 📚\n"
        "• Organiza tu tiempo con un horario.\n"
        "• Toma descansos regulares (5-10 minutos cada hora).\n"
        "• Duerme lo suficiente y come bien.\n"
        "• ¡No dudes en pedir ayuda a tus profesores o compañeros si la necesitas!"
    )

# Comando /psicologia: Informacion del departamento de psicologia
async def psicologia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Si necesitas apoyo profesional, el Departamento de Psicología Escolar está para ayudarte. 📞\n"
        "**Teléfono:** [Tu número de teléfono del departamento]\n"
        "**Correo Electrónico:** [Tu correo electrónico del departamento]\n"
        "**Horario:** Lunes a Viernes, [Tu horario de atención]\n"
        "**Ubicación:** [Tu ubicación o enlace a un mapa]\n"
        "También puedes visitar su página web para más información: [Tu enlace a la web del departamento]\n"
        "Recuerda, ¡buscar ayuda es un paso muy valiente y positivo para tu bienestar!"
    )

# Manejador de mensajes de texto: Respuesta a palabras clave (ejemplo simple)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower() # Convertir a minúsculas para facilitar la detección

    if "estrés" in text or "ansiedad" in text or "abrumado" in text:
        await update.message.reply_text(
            "Entiendo que te sientas así. Es normal experimentar estrés o ansiedad. "
            "¿Te gustaría que te ofrezca un ejercicio de /respiracion, "
            "o quizás algunos /tipsestudio? "
            "Si sientes que necesitas hablar con alguien, puedes consultar el comando /psicologia."
        )
    elif "gracias" in text or "gracias!" in text:
        await update.message.reply_text("¡De nada! Estoy aquí para ayudarte cuando lo necesites. 😊")
    else:
        # Respuesta por defecto si no reconoce la intención
        await update.message.reply_text(
            "Lo siento, no estoy seguro de cómo ayudarte con eso. "
            "Puedes usar /ayuda para ver las opciones que tengo disponibles."
        )

# --- 3. Función Principal para Ejecutar el Bot ---
def main() -> None:
    # Crea la aplicación del bot y pásale tu token
    application = Application.builder().token(BOT_TOKEN).build()

    # Registra los manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", ayuda))
    application.add_handler(CommandHandler("respiracion", respiracion))
    application.add_handler(CommandHandler("tipsestudio", tips_estudio))
    application.add_handler(CommandHandler("psicologia", psicologia))

    # Registra un manejador para mensajes de texto (no comandos)
    # filters.TEXT & ~filters.COMMAND asegura que solo procese texto que no sea un comando
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inicia el polling (el bot estará escuchando nuevos mensajes)
    logger.info("Bot started polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# if __name__ == "__main__":
#     from telegram.ext import ContextTypes # Importa aquí para evitar dependencia circular
#     main()