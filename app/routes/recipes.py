from flask import Blueprint, request, render_template, redirect, url_for, flash, abort

# 注意：此模組僅為路由骨架，尚未包含完整實作邏輯。
from app.models.recipe import Recipe

# 我們以 recipes 為核心宣告一組 Blueprint
recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/')
@recipes_bp.route('/recipes')
def index():
    """
    HTTP 方法: GET
    用途: 首頁及食譜清單列表
    邏輯: 讀取 search / category 的 query string 參數，呼叫 Repo 並渲染 'recipes/index.html'。
    """
    pass

@recipes_bp.route('/recipes/new', methods=['GET'])
def new():
    """
    HTTP 方法: GET
    用途: 新增食譜前的表單視圖
    邏輯: 單純載入並渲染 'recipes/new.html' 表單畫面供給使用者。
    """
    pass

@recipes_bp.route('/recipes', methods=['POST'])
def create():
    """
    HTTP 方法: POST
    用途: 接收表單傳入的新食譜資料
    邏輯: 處理並驗證欄位、呼叫 Recipe.create()，然後 redirect() 回到食譜列表。
    """
    pass

@recipes_bp.route('/recipes/<int:id>', methods=['GET'])
def detail(id):
    """
    HTTP 方法: GET
    用途: 單一筆食譜詳細檢視視圖
    邏輯: 用 id 尋找指定的食譜交由 'recipes/detail.html'；若是空則觸發 404
    """
    pass

@recipes_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    HTTP 方法: GET
    用途: 載入當下食譜供使用者直接編輯的表單視圖
    邏輯: 用 id 選取當前數值，載回 'recipes/edit.html'，供預填寫欄位用。
    """
    pass

@recipes_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update(id):
    """
    HTTP 方法: POST
    用途: 接收編輯視圖的食譜更新結果
    邏輯: 驗證及覆寫資料，完成 Recipe.update() 後，重導向至詳細檢視 (/recipes/<id>)。
    """
    pass

@recipes_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    HTTP 方法: POST
    用途: 從系統完全抹除該食譜
    邏輯: 透過 Recipe.delete(id) 刪除紀錄，接著將使用者退回首頁。
    """
    pass
