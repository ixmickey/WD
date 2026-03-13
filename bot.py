import telebot
import requests
from config import TELEGRAM_TOKEN, APP_URL

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    data = call.data

    if data.startswith("approve_"):
        request_id = data.split("_")[1]
        status = "Approved"

    elif data.startswith("reject_"):
        request_id = data.split("_")[1]
        status = "Rejected"

    else:
        return

    # send update to your Flask server
    requests.post(
        f"{APP_URL}/update_status",
        json={"id": request_id, "status": status}
    )

    bot.answer_callback_query(call.id, status)

    bot.edit_message_text(
        f"{status}",
        call.message.chat.id,
        call.message.message_id
    )

bot.infinity_polling()
