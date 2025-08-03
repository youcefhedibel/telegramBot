import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue 😊\n"
        "Envoyez-moi un numéro comme :\n"
        "📱 0550121212 ou 550121212\n"
        "et je le convertirai en ➡️ +213550121212"
    )

async def convert_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = update.message.text.strip()
    num = re.sub(r"[^\d+]", "", num)  # garde seulement chiffres et +

    # ✅ Si le numéro commence par "0" → on enlève et ajoute +213
    if num.startswith("0") and len(num) >= 9:
        international_num = "+213" + num[1:]
        await update.message.reply_text(international_num)

    # ✅ Si le numéro commence directement par 5xx...
    elif num.startswith(("5", "6", "7")) and len(num) >= 8:
        international_num = "+213" + num
        await update.message.reply_text(international_num)

    # ✅ Si déjà au format international
    elif num.startswith("+213"):
        await update.message.reply_text("✅ Ce numéro est déjà au format international.")

    else:
        await update.message.reply_text("⚠️ Numéro invalide.\nExemple : 0550505050 ou 550505050")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_number))

    print("🤖 Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
