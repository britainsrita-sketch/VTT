import logging
from datetime import date
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get token from environment variable (set this in Railway dashboard)
TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am your Age Calculator Bot.\n"
        "Please send your birthdate in this format: DD/MM/YYYY\n"
        "Example: 15/08/1995"
    )

async def calculate_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        day, month, year = map(int, user_input.split('/'))
        birthdate = date(year, month, day)
        today = date.today()
        
        if birthdate > today:
            await update.message.reply_text("Birthdate cannot be in the future!")
            return

        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        await update.message.reply_text(f"You are {age} years old.")
    
    except ValueError:
        await update.message.reply_text("Invalid format! Please use DD/MM/YYYY (e.g., 15/08/1995).")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_age))
    
    print("Bot is running...")
    app.run_polling()
