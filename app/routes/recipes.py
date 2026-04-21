from flask import Blueprint, request, render_template, redirect, url_for, flash, abort

from app.models.recipe import Recipe

# 我們以 recipes 為核心宣告一組 Blueprint
recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/')
@recipes_bp.route('/recipes')
def index():
    """首頁及食譜清單列表"""
    search_query = request.args.get('q', '').strip()
    category_filter = request.args.get('category', '').strip()
    
    recipes_list = Recipe.get_all(
        search_query=search_query if search_query else None,
        category_filter=category_filter if category_filter else None
    )
    return render_template('recipes/index.html', recipes=recipes_list, q=search_query, category=category_filter)

@recipes_bp.route('/recipes/new', methods=['GET'])
def new():
    """新增食譜前的表單視圖"""
    return render_template('recipes/new.html')

@recipes_bp.route('/recipes', methods=['POST'])
def create():
    """接收表單傳入的新食譜資料並建立"""
    title = request.form.get('title', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    instructions = request.form.get('instructions', '').strip()
    category = request.form.get('category', '').strip()
    
    # 基本必填欄位驗證
    if not title or not ingredients or not instructions or not category:
        flash('所有欄位皆為必填，請檢查後再送出。', 'danger')
        # 驗證失敗時，帶著剛剛填的資料重新渲染表單頁
        return render_template('recipes/new.html', 
                               title=title, 
                               ingredients=ingredients, 
                               instructions=instructions, 
                               category=category)
                               
    recipe_id = Recipe.create(title, ingredients, instructions, category)
    if recipe_id:
        flash('新增食譜成功！', 'success')
        return redirect(url_for('recipes.index'))
    else:
        flash('發生內部錯誤，新增食譜失敗。', 'danger')
        return render_template('recipes/new.html', 
                               title=title, 
                               ingredients=ingredients, 
                               instructions=instructions, 
                               category=category)

@recipes_bp.route('/recipes/<int:id>', methods=['GET'])
def detail(id):
    """單一筆食譜詳細檢視視圖"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
    return render_template('recipes/detail.html', recipe=recipe)

@recipes_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit(id):
    """載入當下食譜供使用者直接編輯的表單視圖"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
    return render_template('recipes/edit.html', recipe=recipe)

@recipes_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update(id):
    """接收編輯視圖的食譜更新結果"""
    # 確保原本的食譜存在
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    title = request.form.get('title', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    instructions = request.form.get('instructions', '').strip()
    category = request.form.get('category', '').strip()
    
    if not title or not ingredients or not instructions or not category:
        flash('所有欄位皆為必填，請檢查後再送出。', 'danger')
        # 組裝原本的 ID，讓編輯頁不報錯
        err_recipe = {
            'id': id,
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions,
            'category': category
        }
        return render_template('recipes/edit.html', recipe=err_recipe)
        
    success = Recipe.update(id, title, ingredients, instructions, category)
    if success:
        flash('食譜已成功更新！', 'success')
        return redirect(url_for('recipes.detail', id=id))
    else:
        flash('更新食譜失敗。', 'danger')
        return redirect(url_for('recipes.edit', id=id))

@recipes_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """從系統完全抹除該食譜"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    success = Recipe.delete(id)
    if success:
        flash('食譜已順利刪除。', 'success')
    else:
        flash('刪除食譜失敗。', 'danger')
        
    return redirect(url_for('recipes.index'))
