import logging
import os
import pytz
from telegram import Bot
from telegram.ext import Updater, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load token and channel ID from environment
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def generate_result():
    india_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(india_tz)
    hour_min = now.strftime("%I:%M %p")

    lucky_number = random.randint(0, 9)
    lucky_jodi = f"{random.randint(0, 9)}{random.randint(0, 9)}"
    round_time = hour_min

    message = f"🎰 Mafia Matka Result\n\n⏰ Time: {round_time}\n🔢 Lucky No: {lucky_number}\n🔗 Lucky Jodi: {lucky_jodi}"
    bot.send_message(chat_id=CHANNEL_ID, text=message)

def main():
    global bot
    bot = Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_result, trigger='interval', minutes=15)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
