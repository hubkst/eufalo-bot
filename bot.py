import os
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

keyboard = [
    ["📚 Глаголы недели", "🃏 Флеш-карты"],
    ["✍️ Упражнения", "📖 Грамматика"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! 🇵🇹 Я бот для изучения европейского португальского языка.",
        reply_markup=markup,
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📚 Глаголы недели":
        await update.message.reply_text("Скоро здесь появятся глаголы недели 🇵🇹")

    elif text == "🃏 Флеш-карты":
        await update.message.reply_text("Флеш-карты в разработке 🃏")

    elif text == "✍️ Упражнения":
        await update.message.reply_text("Упражнения скоро будут ✍️")

    elif text == "📖 Грамматика":
        await update.message.reply_text("Раздел грамматики готовится 📖")


application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))


@app.route("/")
def home():
    return "Bot is running"


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"


if __name__ == "__main__":
    import asyncio

    async def main():
        await application.initialize()
        await application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
        await application.start()

    asyncio.run(main())
