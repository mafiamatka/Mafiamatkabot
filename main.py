import logging
import random
import time
import threading
from datetime import datetime
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

TOKEN = '8061917597:AAE1MLDN2c96zV8mzPe8rYItJOvIHx9ZFvI'  # ✅ Bot token set
CHANNEL_ID = '@mafiamatka'                                # ✅ Channel ID set

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

round_number = 1
bets = []

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Mafia Matka Bot is running.")

def bet(update: Update, context: CallbackContext):
    try:
        amount = int(context.args[0])
        if amount < 10:
            update.message.reply_text("❌ Minimum bet is ₹10.")
            return
        bets.append({
            'username': update.message.from_user.username or "unknown",
            'amount': amount
        })
        update.message.reply_text("✅ Bet placed.")
    except:
        update.message.reply_text("❌ Use format: /bet <amount>")

def generate_result():
    global round_number, bets

    while True:
        time.sleep(900)  # 15 minutes
        if bets:
            winner = min(bets, key=lambda x: x['amount'])
        else:
            winner = None

        lucky_no = random.randint(0, 9)
        jodi = f"{random.randint(0, 9)}-{random.randint(0, 9)}"

        result_msg = f"🎲 Round No: {round_number}\n"
        result_msg += f"🎯 Lucky No: {lucky_no}\n"
        result_msg += f"💞 Lucky Jodi: {jodi}\n\n"
        result_msg += f"🚨 Round {round_number + 1} has started!"

        bot.send_message(chat_id=CHANNEL_ID, text=result_msg)

        round_number += 1
        bets = []

# Register command handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('bet', bet))

# Start the bot
updater.start_polling()

# Start result loop
threading.Thread(target=generate_result, daemon=True).start()
