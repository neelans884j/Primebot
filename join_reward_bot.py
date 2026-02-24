import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# ===== CONFIG =====
BOT_TOKEN = os.getenv("7583310443:AAHXM6923gsdx1SN6XLf4phXMX2L8ljLbkQ")  # Telegram bot token
REQUIRED_CHANNELS = ["@primehorizons", "@techyqrcode", "@phrestart2026"]  # Replace with your channels
REWARD_FILE_PATH = "https://drive.google.com/drive/folders/1Rz5hIKL4SHitlkCB7DreeNy5YPjPNrrq"  # File to send
# ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✅ I Joined", callback_data="check_join")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Join all the required channels and then press 'I Joined'.",
        reply_markup=reply_markup
    )

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()  # acknowledge the button click

    all_joined = True
    for channel in REQUIRED_CHANNELS:
        member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status not in ["member", "administrator", "creator"]:
            all_joined = False
            break

    if all_joined:
        # Send personal reward file
        await context.bot.send_document(chat_id=user_id, document=open(REWARD_FILE_PATH, "rb"))
        await query.edit_message_text(
            "✅ Congrats! You joined all channels! Your reward has been sent to you personally.",
            parse_mode=ParseMode.HTML
        )
    else:
        # Still not joined all channels
        channels_text = "\n".join(REQUIRED_CHANNELS)
        keyboard = [[InlineKeyboardButton("✅ I Joined", callback_data="check_join")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"❌ You must join all channels first:\n{channels_text}\n\nThen press 'I Joined' again.",
            reply_markup=reply_markup
        )

# ===== Application =====
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

# ===== Run Polling =====
app.run_polling()
