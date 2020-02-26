import sqlite3
database = "/Users/arturyakushev/Documents/GitHub/Telegram_bot/testbd.db"
conn = sqlite3.connect(database)
conn.close()