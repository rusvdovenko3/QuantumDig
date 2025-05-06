# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import sqlite3
import time
from config import TOKEN

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 0,
    hashrate REAL DEFAULT 1,
    last_mine INTEGER DEFAULT 0,
    ref_by INTEGER
)''')
conn.commit()

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    args = context.args
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone() is None:
        ref_by = int(args[0]) if args else None
        cursor.execute("INSERT INTO users (user_id, ref_by) VALUES (?, ?)", (user_id, ref_by))
        conn.commit()
        if ref_by:
            cursor.execute("UPDATE users SET balance = balance + 1 WHERE user_id=?", (ref_by,))
            conn.commit()
    update.message.reply_text("Добро пожаловать в Quantum Dig! Напиши /mine чтобы начать добычу.")

def mine(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    now = int(time.time())
    cursor.execute("SELECT balance, hashrate, last_mine FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row:
        balance, hashrate, last_mine = row
        elapsed = now - last_mine
        mined = elapsed * hashrate * 0.0001
        balance += mined
        cursor.execute("UPDATE users SET balance=?, last_mine=? WHERE user_id=?", (balance, now, user_id))
        conn.commit()
        update.message.reply_text(f"Вы добыли {mined:.6f} XRP. Баланс: {balance:.6f} XRP")
    else:
        update.message.reply_text("Сначала напиши /start.")

def balance(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row:
        update.message.reply_text(f"Ваш баланс: {row[0]:.6f} XRP")
    else:
        update.message.reply_text("Сначала напиши /start.")

def invite(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    update.message.reply_text(f"Приглашай друзей: https://t.me/{context.bot.username}?start={user_id}")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mine", mine))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("invite", invite))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
