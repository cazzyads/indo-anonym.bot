import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

waiting_users = []
partners = {}

keyboard = ReplyKeyboardMarkup(
    [["🔎 Cari Teman", "⏭ Next"], ["⛔ Stop"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Selamat datang di Indo Anonymous Bot!\\n\\nTekan 🔎 Cari Teman untuk mulai chat anonim.",
        reply_markup=keyboard
    )

async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot sedang disiapkan. Tahap selanjutnya kita deploy ke Railway.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay))
    app.run_polling()

if __name__ == "__main__":
    main()
