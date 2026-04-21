import sqlite3
from .database import get_db_connection

class Recipe:
    @staticmethod
    def create(title, ingredients, instructions, category):
        """
        新增一筆食譜記錄
        參數: title, ingredients, instructions, category
        回傳: 寫入成功的紀錄 ID，若發生 SQLite 錯誤則回傳 None
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recipes (title, ingredients, instructions, category)
                VALUES (?, ?, ?, ?)
            ''', (title, ingredients, instructions, category))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[Model Error] 新增食譜時發生錯誤: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all(search_query=None, category_filter=None):
        """
        取得所有記錄 (支援搜尋字詞與分類過濾)
        回傳: dict 字典陣列，若發生資料庫錯誤則回傳空陣列 []
        """
        conn = None
        try:
            conn = get_db_connection()
            query = 'SELECT * FROM recipes WHERE 1=1'
            params = []
            
            if search_query:
                query += ' AND title LIKE ?'
                params.append(f'%{search_query}%')
                
            if category_filter:
                query += ' AND category = ?'
                params.append(category_filter)
                
            query += ' ORDER BY created_at DESC'
            
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[Model Error] 讀取所有食譜時發生錯誤: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        """
        取得單筆記錄
        參數: recipe_id (食譜唯一碼)
        回傳: 單一 dict 字典物件，若找不到或發生錯誤則回傳 None
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[Model Error] 讀取單筆食譜時發生錯誤: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update(recipe_id, title, ingredients, instructions, category):
        """
        更新記錄
        參數: recipe_id 以及所有需替換的新欄位資料
        回傳: bool 成功回傳 True，發生錯誤或是未變更回傳 False
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE recipes 
                SET title = ?, ingredients = ?, instructions = ?, category = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (title, ingredients, instructions, category, recipe_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[Model Error] 更新食譜時發生錯誤: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(recipe_id):
        """
        刪除記錄
        參數: recipe_id
        回傳: bool 刪除成功回傳 True，發生錯誤或未刪除回傳 False
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[Model Error] 刪除食譜時發生錯誤: {e}")
            return False
        finally:
            if conn:
                conn.close()
