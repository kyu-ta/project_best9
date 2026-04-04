from flask import Flask
from flask_admin.contrib.sqla import ModelView
from config import Config
from .extensions import db, migrate, admin, login_manager

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    from .routes import main
    app.register_blueprint(main)
    from .auth import auth
    app.register_blueprint(auth)
    
    from app import models
    target_models = [models.Team, models.Position, models.Player, models.BestNine, models.BestNineSlot]
    for model in target_models:
        admin.add_view(ModelView(model, db.session))

    return app