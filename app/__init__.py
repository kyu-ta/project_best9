from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name="管理画面", theme=Bootstrap4Theme())

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    from .routes import main
    app.register_blueprint(main)
    
    from app import models
    target_models = [models.Team, models.Position, models.Player, models.BestNine, models.BestNineSlot]
    for model in target_models:
        admin.add_view(ModelView(model, db.session))

    return app