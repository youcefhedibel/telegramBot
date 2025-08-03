import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # On récupère le token depuis Render

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue 😊\n"
        "Envoyez-moi un numéro comme :\n"
        "📱 0550121212\n"
        "et je le convertirai en ➡️ +213550121212"
    )

async def convert_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = update.message.text.strip()

    # Supprimer tout sauf les chiffres et le "+"
    num = re.sub(r"[^\d+]", "", num)

    if num.startswith("0") and len(num) >= 9:
        international_num = "+213" + num[1:]
        await update.message.reply_text(international_num)
    elif num.startswith("+213"):
        await update.message.reply_text("✅ Ce numéro est déjà au format international.")
    else:
        await update.message.reply_text("⚠️ Numéro invalide.\nExemple attendu : 0550121212")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_number))

    print("🤖 Bot démarré...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
