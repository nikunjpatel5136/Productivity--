from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    
    
    app.config["SECRET KEY"] = "Bot"
    app.secret_key = "Bot"
    
    #Set path to where database needs to be saved
    db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    db.init_app(app)
        
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")
    
    from .models import User, Note                              #import classes from models
    
    with app.app_context():
        db.create_all()
        
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #telling Flask what user to look for here
    
    return app
