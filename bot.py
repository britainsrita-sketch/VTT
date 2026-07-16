import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from database import init_db, save_item, get_items

# Initialize database on startup
init_db()

async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /save [category] [link/text]")
        return
    category = context.args[0]
    content = " ".join(context.args[1:])
    save_item(category, content)
    await update.message.reply_text(f"Saved to {category}!")

async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /view [category]")
        return
    category = context.args[0]
    items = get_items(category)
    if items:
        await update.message.reply_text(f"Items in {category}:\n" + "\n".join(items))
    else:
        await update.message.reply_text("No items found in this category.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("save", save))
    app.add_handler(CommandHandler("view", view))
    app.run_polling()
