import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
from pln_respuestas import generar_respuesta

# --- 1. Configuración Inicial ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token de tu bot
BOT_TOKEN = "7550990980:AAFB5oGvg4GC_zstquoXOgIUbqtop1rRKqI"

# --- 2. Comandos ---
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Aquí tienes algunas cosas que puedo hacer:\n"
        "/respiracion - Te guío en un ejercicio de respiración.\n"
        "/tipsestudio - Consejos para manejar el estrés académico.\n"
        "/psicologia - Información para contactar al departamento de psicología.\n"
        "También puedes escribirme cómo te sientes y veré cómo puedo ayudarte."
    )

async def respiracion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🌬️ **Ejercicio de Respiración para Calmar la Ansiedad** 🧘‍♂️\n\n"
        "Vamos a hacer una técnica llamada **4-7-8**. Te ayudará a calmar tu mente y cuerpo. Empecemos:\n\n"
        "🔹 *Paso 1:* Inhala lentamente por la nariz mientras cuentas hasta **4**...\n"
        "🔹 *Paso 2:* Mantén el aire en tus pulmones mientras cuentas hasta **7**...\n"
        "🔹 *Paso 3:* Exhala suavemente por la boca mientras cuentas hasta **8**...\n\n"
        "Repite esto entre 3 y 5 veces. Cierra los ojos si lo deseas, y enfócate solo en tu respiración. 🍃\n\n"
        "🗨️ *¿No te funcionó?* Puedes seguir charlando conmigo para ver si puedo ayudarte, "
        "o incluso usar el comando /cita para agendar una sesión personalizada. 🤝",
        parse_mode="Markdown"
    )



async def tips_estudio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📘 **Tips para Manejar el Estrés Académico**\n\n"
        "Aquí tienes algunas recomendaciones que pueden ayudarte a estudiar con más calma y eficacia:\n\n"
        "🔹 *Organiza tu tiempo* con un horario realista y flexible.\n"
        "🔹 *Toma descansos* regulares (5 a 10 minutos cada hora).\n"
        "🔹 *Duerme bien* y mantén una alimentación balanceada.\n"
        "🔹 *Habla con tus profesores o compañeros* si necesitas apoyo.\n\n"
        "💡 *¿Te sigues sintiendo abrumado?* Puedes seguir conversando conmigo o usar el comando /cita para agendar una charla personalizada. 🤝",
        parse_mode="Markdown"
    )


async def psicologia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🧠 **Apoyo Profesional - Psicología Escolar**\n\n"
        "Si estás pasando por un momento difícil o necesitas hablar con alguien, el Departamento de Psicología Escolar está disponible para ti. Aquí tienes sus datos de contacto:\n\n"
        "📞 **Teléfono:** +52 833 123 4567\n"
        "📧 **Correo Electrónico:** psicologia@tuinstituto.edu.mx\n"
        "🕐 **Horario de atención:** Lunes a Viernes, 8:00 a.m. - 3:00 p.m.\n"
        "📍 **Ubicación:** Edificio C, planta alta (ver mapa: [Ubicación en Google Maps](https://maps.google.com))\n"
        "🌐 **Sitio web:** [Visita la página oficial](https://www.tuinstituto.edu.mx/psicologia)\n\n"
        "Recuerda: pedir ayuda también es una forma de cuidar de ti. 🤝",
        parse_mode="Markdown"
    )


# --- 3. PLN ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensaje = update.message.text
    respuesta = generar_respuesta(mensaje)
    await update.message.reply_text(respuesta)

# --- 4. Cita (ConversationHandler) ---
ELEGIR_DIA, ELEGIR_HORA, ELEGIR_TEMA = range(3)

async def iniciar_cita(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("¿Qué día te gustaría agendar tu cita? (ej. lunes, 20 de julio)")
    return ELEGIR_DIA

async def recibir_dia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["dia"] = update.message.text
    await update.message.reply_text("¿A qué hora deseas tu cita? (ej. 10:00 AM)")
    return ELEGIR_HORA

async def recibir_hora(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["hora"] = update.message.text
    await update.message.reply_text("¿Cuál es el motivo de tu cita?")
    return ELEGIR_TEMA

async def recibir_tema(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["tema"] = update.message.text
    dia = context.user_data["dia"]
    hora = context.user_data["hora"]
    tema = context.user_data["tema"]
    await update.message.reply_text(
        f"Tu cita ha sido registrada:\n📅 Día: {dia}\n🕐 Hora: {hora}\n📝 Motivo: {tema}\n\n"
        "¡Gracias! Te esperamos. 😊"
    )
    return ConversationHandler.END

async def cancelar_cita(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Has cancelado el proceso de agendar cita.")
    return ConversationHandler.END

# --- 5. Main ---
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("ayuda", ayuda))
    application.add_handler(CommandHandler("respiracion", respiracion))
    application.add_handler(CommandHandler("tipsestudio", tips_estudio))
    application.add_handler(CommandHandler("psicologia", psicologia))

    # Conversación para citas
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

    # Mensajes normales
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot iniciado correctamente.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()  