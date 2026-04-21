from .database import get_db_connection

class Recipe:
    @staticmethod
    def create(title, ingredients, instructions, category):
        """
        新增一筆食譜
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recipes (title, ingredients, instructions, category)
            VALUES (?, ?, ?, ?)
        ''', (title, ingredients, instructions, category))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all(search_query=None, category_filter=None):
        """
        取得所有食譜。
        若有給定 search_query 可對 title 做模糊搜尋
        若有給定 category_filter 則只過濾出特定分類
        """
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
        conn.close()
        
        # 轉成一般的 Python list of dict 好操作
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(recipe_id):
        """
        依 ID 取得單筆食譜
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(recipe_id, title, ingredients, instructions, category):
        """
        更新特定 ID 的食譜資料，並將 updated_at 更新為當前時間
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE recipes 
            SET title = ?, ingredients = ?, instructions = ?, category = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, ingredients, instructions, category, recipe_id))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0

    @staticmethod
    def delete(recipe_id):
        """
        刪除特定 ID 的食譜
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
