import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "7583310443:AAHXM6923gsdx1SN6XLf4phXMX2L8ljLbkQ"

CHANNEL_1 = "@primehorizons"
CHANNEL_2 = "@phrestart2026"
CHANNEL_3 = "@techyqrcode"

bot = telebot.TeleBot(BOT_TOKEN)

def check_member(user_id, channel):
    try:
        status = bot.get_chat_member(channel, user_id).status
        return status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if (check_member(user_id, CHANNEL_1) and
        check_member(user_id, CHANNEL_2) and
        check_member(user_id, CHANNEL_3)):

        bot.send_message(message.chat.id, "✅ Access Granted 🔥 Welcome To Prime Horizons")

    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Join Channel 1", url=f"https://t.me/{CHANNEL_1.replace('@','')}"))
        markup.add(InlineKeyboardButton("📢 Join Channel 2", url=f"https://t.me/{CHANNEL_2.replace('@','')}"))
        markup.add(InlineKeyboardButton("📢 Join Channel 3", url=f"https://t.me/{CHANNEL_3.replace('@','')}"))
        markup.add(InlineKeyboardButton("✅ I Joined", callback_data="check"))

        bot.send_message(message.chat.id, "🔒 Please Join All Required Channels First!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback_check(call):
    user_id = call.from_user.id

    if (check_member(user_id, CHANNEL_1) and
        check_member(user_id, CHANNEL_2) and
        check_member(user_id, CHANNEL_3)):

        bot.edit_message_text("✅ Access Granted 🔥 Welcome To Prime Horizons",
                              call.message.chat.id,
                              call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ Still Not Joined All Channels!", show_alert=True)

bot.infinity_polling()
