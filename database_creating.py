import sqlite3

conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

# Создание таблицы с играми
cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player1 TEXT,
        player2 TEXT,
        coordinates TEXT,
        flag INTEGER, 
        result
    )
''')

# Создание таблицы с игроками
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')

conn.close()
