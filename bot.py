import os
import sys
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# 1. Force logs to show up immediately in Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)

async def start(update, context):
    await update.message.reply_text("Bot is online and ready!")

async def echo(update, context):
    # This will reply to any text message
    await update.message.reply_text(f"You said: {update.message.text}")

if __name__ == '__main__':
    # 2. Get token from Railway Variable
    token = os.environ.get("TELEGRAM_TOKEN")
    
    if not token:
        logging.error("TELEGRAM_TOKEN is missing! Please set it in Railway Variables.")
        sys.exit(1)

    logging.info("Starting bot...")
    
    # 3. Build application
    app = ApplicationBuilder().token(token).build()
    
    # 4. Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    # 5. Run with polling
    logging.info("Bot is polling for updates...")
    app.run_polling()
