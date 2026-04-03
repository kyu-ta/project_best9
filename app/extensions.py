from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name="管理画面", theme=Bootstrap4Theme())
login_manager = LoginManager()
