import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

CHOOSE_DRINK, CHOOSE_TYPE = range(2)

OWNER_IDS = [] # to insert user id  info 

DRINKS = [
    "Americano", "Cafe Latte", "Cappuccino Assassino", "Caramel Latte", "Mocha", "Matcha Latte","Caramel Matcha Latte", "Pure Matcha","Hot Chocolate", "Bandung"
]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start (update:Update, context:ContextTypes.DEFAULT_TYPE): 
    welcome_text = (
        "👋 Hello! We are Daily Dose and we are all about coffee☕, matcha🍵 and vibes✨\n\n"
        "Please choose your drink:"
    )
    reply_keyboard = [[drink] for drink in DRINKS]
    await update.message.reply_text(
        welcome_text,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSE_DRINK

async def choose_drink(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data ['drink'] = update.message.text
    reply_keyboard = [['Hot'], ['Iced']]
    await update.message.reply_text(
        "Do you want it hot or iced?"
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSE_TYPE

async def choose_type (update:Update, context:ContextTypes.DEFAULT_TYPE): 
    context.user_data ['type'] = update.message.text
    drink = context.user_data.get("drink")
    type = context.user_data.get("type")
    username = update.message.from_user.username or update.message.from_user.full_name

    order_message = (
        f"📥 New Order Received!\n"
        f"👤 Username: @{username}\n"
        f"🥤 Drink: {drink}\n"
        f"🔥 Type: {type_}"

    )

    #contact each owner_id
    for owner_id in OWNER_IDS: 
        await context.bot.send_message(chat_id=owner_id, text=order_message)

    await update.message.reply_text("✅ Order received! We'll let you know when it's ready.")
    return ConversationHandler.END

    # async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     await update.message.reply_text('❌ Order cancelled. You can start again by sending /start.')
    #     return ConversationHandler.END

def main(): 
    YOUR_BOT_TOKEN = "" # insert bot token 
    app = ApplicationBuilder().token(YOUR_BOT_TOKEN).build()

    conversation_handler = ConversationHandler (
        entry_points=[CommandHandler("start", start)]
        states={
            CHOOSE_DRINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_drink)],
            CHOOSE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_type)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conversation_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
