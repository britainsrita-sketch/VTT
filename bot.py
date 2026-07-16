import os
import sys
import logging
import sqlite3
from telegram.ext import ApplicationBuilder, CommandHandler

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)

# --- Database Functions ---
def init_db():
    conn = sqlite3.connect("archive.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS archive 
                      (id INTEGER PRIMARY KEY, category TEXT, content TEXT)''')
    conn.commit()
    conn.close()

# --- Bot Commands ---
async def start(update, context):
    await update.message.reply_text("QuickStudy Archive is ready! Use /save [category] [text] to archive, and /view [category] to see your saved items.")

async def save(update, context):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /save [category] [content]")
        return
    category = context.args[0]
    content = " ".join(context.args[1:])
    
    conn = sqlite3.connect("archive.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO archive (category, content) VALUES (?, ?)", (category, content))
    conn.commit()
    conn.close()
    
    await update.message.reply_text(f"✅ Saved to *{category}*!", parse_mode='Markdown')

async def view(update, context):
    if not context.args:
        await update.message.reply_text("Usage: /view [category]")
        return
    category = context.args[0]
    
    conn = sqlite3.connect("archive.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM archive WHERE category = ?", (category,))
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        items = "\n".join([f"• {row[0]}" for row in rows])
        await update.message.reply_text(f"📁 *{category.upper()}* items:\n\n{items}", parse_mode='Markdown')
    else:
        await update.message.reply_text(f"No items found in {category}.")

if __name__ == '__main__':
    init_db()
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("save", save))
    app.add_handler(CommandHandler("view", view))
    
    app.run_polling()
