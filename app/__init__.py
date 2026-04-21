import os
from flask import Flask
from .routes.recipes import recipes_bp

def create_app():
    app = Flask(__name__)
    
    # 基本設定 (使用環境變數或預設值)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 註冊 Blueprints 路由
    app.register_blueprint(recipes_bp)
    
    return app
