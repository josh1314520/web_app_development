import sqlite3
import os

# 依照 implementation skill 規定，將 SQLite DB 存放在 instance/database.db
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance')
DB_PATH = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    """
    取得資料庫連線，並設定 row_factory 使回傳值可如同字典一般透過 key 取得對應欄位
    """
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    執行 database/schema.sql 初始化資料庫 (若尚未建立則建表)
    """
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        conn = None
        try:
            conn = get_db_connection()
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
        except sqlite3.Error as e:
            print(f"資料庫初始化發生錯誤: {e}")
        finally:
            if conn:
                conn.close()
