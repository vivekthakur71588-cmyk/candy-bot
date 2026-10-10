import os
import threading
from flask import Flask
import telebot

# --- KEEP-ALIVE SERVER FOR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Candy Buddies Bot is running 24/7!", 200

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Background thread me web server start hoga
threading.Thread(target=run_web, daemon=True).start()
# -----------------------------------

# Yahan se aapka telebot ka code continue hoga:
# bot = telebot.TeleBot("YOUR_BOT_TOKEN")
# ... handlers ...
# bot.infinity_polling()
import telebot
from telebot import types

BOT_TOKEN = "8790497507:AAHvYj8iseRkFfqAV3IQq4hFTKM7wxAUImc"
WEBAPP_URL = "https://candy-buddies.vercel.app"
ADMIN_ID = 8148784879
PAYOUT_CHANNEL = "https://t.me/candybuddiespayout"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    caption_text = (
        f"🍭🌾 *Welcome to Candy Buddies, {user_name}!* 🌾🍭\n\n"
        "🐮 *Build your sweet farm, collect rewards & grow your earnings!*\n"
        "🍬 *Watch ads, complete tasks, farm & invite friends.*\n"
        "🎁 *Start your Candy Buddies journey today!*\n\n"
        "🚀 *Tap START FARMING below and let the fun begin!* 🍭✨"
    )
    markup = types.InlineKeyboardMarkup()
    web_app_info = types.WebAppInfo(url="https://candy-buddy-earn.vercel.app/")
    btn_start = types.InlineKeyboardButton("🚀 START FARMING 🍭", web_app=web_app_info)
    markup.add(btn_start)
    bot.send_message(message.chat.id, caption_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['approve'])
def approve_payment(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Unauthorized! Admin access only.")
        return

    args = message.text.split(maxsplit=3)
    if len(args) < 4:
        bot.reply_to(message, "⚠ Invalid format!\nUsage: `/approve <USER_ID> <AMOUNT> <TON_TX_HASH>`", parse_mode='Markdown')
        return

    target_user_id, amount, tx_hash = args[1], args[2], args[3]
    user_receipt = (
        "🎉 *Withdrawal Approved!*\n\n"
        "Your Candy Buddies payout has been successfully transferred.\n\n"
        f"💰 *Amount:* `{amount} CANDY`\n"
        "⚡ *Network:* TON Blockchain\n"
        f"🔍 *Tx Hash / Track ID:* `{tx_hash}`\n\n"
        "📢 Check our official channel for live payout proofs & updates:\n"
        f"👉 [Join Payout Channel]({PAYOUT_CHANNEL})\n\n"
        "Thank you for being part of Candy Buddies! 🍭"
    )
    receipt_markup = types.InlineKeyboardMarkup()
    receipt_markup.add(types.InlineKeyboardButton("📢 View Payout Channel", url=PAYOUT_CHANNEL))

    try:
        bot.send_message(target_user_id, user_receipt, parse_mode='Markdown', reply_markup=receipt_markup)
        bot.reply_to(message, f"✅ User `{target_user_id}` has been notified with payout details!")
    except Exception as e:
        bot.reply_to(message, f"❌ Delivery failed: {e}")

bot.infinity_polling()
  
