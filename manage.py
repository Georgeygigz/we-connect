from flask_mail import Mail

from config import AppConfig
from main import create_app

app = create_app(AppConfig)
mail = Mail(app)

if __name__ == '__main__':
    app.run()
