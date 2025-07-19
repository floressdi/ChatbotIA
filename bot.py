import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters,ConversationHandler
from pln_respuestas import generar_respuesta


# --- 1. Configuración Inicial ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token de tu bot
BOT_TOKEN = "7550990980:AAFB5oGvg4GC_zstquoXOgIUbqtop1rRKqI"





# Comando /ayuda
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Aquí tienes algunas cosas que puedo hacer:\n"
        "/respiracion - Te guío en un ejercicio de respiración.\n"
        "/tipsestudio - Consejos para manejar el estrés académico.\n"
        "/psicologia - Información para contactar al departamento de psicología.\n"
        "También puedes escribirme cómo te sientes y veré cómo puedo ayudarte."
    )

# Comando /respiracion
async def respiracion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "¡Claro! Vamos a hacer un ejercicio de respiración profunda. 🧘‍♀️\n"
        "1. Inhala lentamente por la nariz contando hasta 4.\n"
        "2. Sostén la respiración contando hasta 7.\n"
        "3. Exhala lentamente por la boca contando hasta 8.\n"
        "Repite esto 3-5 veces. Concéntrate solo en tu respiración."
    )

# Comando /tipsestudio
async def tips_estudio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Aquí tienes algunos tips para manejar el estrés académico: 📚\n"
        "• Organiza tu tiempo con un horario.\n"
        "• Toma descansos regulares (5-10 minutos cada hora).\n"
        "• Duerme lo suficiente y come bien.\n"
        "• ¡No dudes en pedir ayuda a tus profesores o compañeros si la necesitas!"
    )

# Comando /psicologia
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
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensaje = update.message.text
    respuesta = generar_respuesta(mensaje)
    await update.message.reply_text(respuesta)

#lo de cita
ELEGIR_DIA, ELEGIR_HORA, ELEGIR_TEMA = range(3)
async def iniciar_cita(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("¿Qué día te gustaría agendar tu cita? (ej. lunes, 20 de julio)")
    return ELEGIR_DIA

async def recibir_dia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    dia = update.message.text
    context.user_data["dia"] = dia
    print(f"[DEBUG] Día guardado: {dia}")  # <---- Agrega esto para ver en la consola

    await update.message.reply_text("¿A qué hora deseas tu cita? (ej. 10:00 AM)")
    return ELEGIR_HORA


async def recibir_hora(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    hora = update.message.text
    context.user_data["hora"] = hora
    print(f"[DEBUG] Hora guardada: {hora}")
    print(f"[DEBUG] Context user_data hasta ahora: {context.user_data}")

    await update.message.reply_text("¿Cuál es el motivo de tu cita?")
    return ELEGIR_TEMA

async def recibir_tema(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tema = update.message.text
    context.user_data["tema"] = tema
    print(f"[DEBUG] Tema guardado: {tema}")
    print(f"[DEBUG] Datos completos de la cita: {context.user_data}")

    dia = context.user_data["dia"]
    hora = context.user_data["hora"]

    await update.message.reply_text(
        f"Tu cita ha sido registrada:\n📅 Día: {dia}\n🕐 Hora: {hora}\n📝 Motivo: {tema}\n\n"
        "¡Gracias! Te esperamos. 😊"
    )
    return ConversationHandler.END


async def cancelar_cita(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Has cancelado el proceso de agendar cita.")
    return ConversationHandler.END


# --- 3. Arranque del bot ---
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Registrar comandos
   
    application.add_handler(CommandHandler("ayuda", ayuda))
    application.add_handler(CommandHandler("respiracion", respiracion))
    application.add_handler(CommandHandler("tipsestudio", tips_estudio))
    application.add_handler(CommandHandler("psicologia", psicologia))

# Conversación para agendar cita
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("cita", iniciar_cita)],
        states={
            ELEGIR_DIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_dia)],
            ELEGIR_HORA: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_hora)],
            ELEGIR_TEMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_tema)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar_cita)],
    )

    application.add_handler(conv_handler)



    # Registrar mensajes normales
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
   
    # Este puede interferir con el flujo del ConversationHandler
        
    # Iniciar polling
    logger.info("Bot iniciado correctamente.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
