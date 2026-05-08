import sqlite3

class DBHelper:

    @staticmethod
    def init_db():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # USERS TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # IDEAS TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            original_idea TEXT,
            improved_idea TEXT,
            domain TEXT,
            uniqueness_score TEXT,
            ai_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # FAVORITES TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            idea_id INTEGER,                      
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
      

        # PREVENT DUPLICATE FAVORITES
        cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS unique_fav 
        ON favorites(user_id, idea_id)
        """)
        
        conn.commit()
        conn.close()

        
   