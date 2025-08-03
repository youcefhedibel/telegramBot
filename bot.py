import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenue !\n\n"
        "Envoyez-moi un numéro au format :\n"
        "📱 0550121212\n"
        "📱 550121212\n"
        "📱 650121212\n"
        "📱 770121212\n\n"
        "Je vous renverrai le format international avec des liens pour WhatsApp et Telegram."
    )

async def convert_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Nettoyage : garder uniquement chiffres et +
    num = re.sub(r"[^\d+]", "", update.message.text.strip())

    # Conversion en format international
    if num.startswith("0") and len(num) >= 9:
        international_num = "+213" + num[1:]
    elif num.startswith(("5", "6", "7")) and len(num) >= 8:
        international_num = "+213" + num
    elif num.startswith("+213"):
        await update.message.reply_text("✅ Ce numéro est déjà au format international.")
        return
    else:
        await update.message.reply_text("⚠️ Numéro invalide.\nExemple : 0550121212 ou 550121212")
        return

    # Liens
    whatsapp_link = f"https://wa.me/{international_num.replace('+', '')}"
    telegram_link = f"https://t.me/{international_num.replace('+', '')}"

    # Boutons
    keyboard = [
        [
            InlineKeyboardButton("📩 Ouvrir dans WhatsApp", url=whatsapp_link),
            InlineKeyboardButton("💬 Ouvrir dans Telegram", url=telegram_link)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Réponse avec boutons
    await update.message.reply_text(
        f"✅ Numéro international : {international_num}",
        reply_markup=reply_markup
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_number))
    print("🤖 Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
