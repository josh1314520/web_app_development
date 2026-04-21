from app import create_app

# 這是主要應用程式實例入口點
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
