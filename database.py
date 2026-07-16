import sqlite3

def init_db():
    conn = sqlite3.connect("archive.db")
    cursor = conn.cursor()
    # Table to store saved items
    cursor.execute('''CREATE TABLE IF NOT EXISTS archive 
                      (id INTEGER PRIMARY KEY, category TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def save_item(category, content):
    conn = sqlite3.connect("archive.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO archive (category, content) VALUES (?, ?)", (category, content))
    conn.commit()
    conn.close()

def get_items(category):
    conn = sqlite3.connect("archive.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM archive WHERE category = ?", (category,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
