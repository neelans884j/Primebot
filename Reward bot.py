from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# ===== CONFIG =====
BOT_TOKEN = "7583310443:AAHXM6923gsdx1SN6XLf4phXMX2L8ljLbkQ"  # <-- Yahan apna bot token daalna
REQUIRED_CHANNELS = ["@primehorizons", "@phrestart2026", "@techyqrcode"]
REWARD_LINK = "https://drive.google.com/drive/folders/1Rz5hIKL4SHitlkCB7DreeNy5YPjPNrrq"
# ==================

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user already joined all channels
    all_joined = True
    for channel in REQUIRED_CHANNELS:
        member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status not in ["member", "administrator", "creator"]:
            all_joined = False
            break

    if all_joined:
        # Already joined → send reward immediately
        await update.message.reply_text(
            f"✅ Congrats! You joined all channels!\nHere is your reward:\n{REWARD_LINK}"
        )
    else:
        # Not joined → show I Joined button
        keyboard = [[InlineKeyboardButton("✅ I Joined", callback_data="check_join")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Welcome! Join all channels and then press 'I Joined'.",
            reply_markup=reply_markup
        )

# ===== CHECK JOIN CALLBACK =====
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()  # acknowledge button click

    all_joined = True
    for channel in REQUIRED_CHANNELS:
        member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status not in ["member", "administrator", "creator"]:
            all_joined = False
            break

    if all_joined:
        # Send reward link
        await query.edit_message_text(
            f"✅ Congrats! You joined all channels!\nHere is your reward:\n{REWARD_LINK}",
            parse_mode=ParseMode.HTML
        )
    else:
        channels_text = "\n".join(REQUIRED_CHANNELS)
        keyboard = [[InlineKeyboardButton("✅ I Joined", callback_data="check_join")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"❌ You must join all channels first:\n{channels_text}\n\nThen press 'I Joined' again.",
            reply_markup=reply_markup
        )

# ===== APPLICATION SETUP =====
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

# ===== RUN POLLING =====
app.run_polling()
