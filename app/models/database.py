import sqlite3
import os

# 預設將 SQLite DB 存放在專案的 database 資料夾中
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'app.db')

def get_db_connection():
    """
    取得資料庫連線，並設定 row_factory 使回傳值可如同字典一般透過 key 取得對應欄位
    """
    # 確保資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    執行 database/schema.sql 初始化資料庫 (若尚未建立則建表)
    """
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        conn = get_db_connection()
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
