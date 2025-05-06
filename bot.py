from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 🔁 ЗАМЕНИ ЭТО НА СВОЮ ССЫЛКУ НА VERCEL
WEBAPP_URL = "https://quantum-dig.vercel.app"

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🚀 Запустить Quantum Dig", web_app={"url": WEBAPP_URL})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Добро пожаловать в Quantum Dig! 👇\nНажми кнопку ниже, чтобы начать майнинг XRP:",
        reply_markup=reply_markup
    )

def main():
    # 🔁 ЗАМЕНИ ЭТО НА СВОЙ ТОКЕН
    updater = Updater("7803039056:AAFOWubc81026s27lGJdTusCk80LZnW9SQo", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
