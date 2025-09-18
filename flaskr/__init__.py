import os

from flask import Flask
from flask_cors import CORS
from flaskr.database import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:Adht7244!@localhost:3306/bookstore"
    CORS(app)
    db.init_app(app)
    import flaskr.models
    with app.app_context():
        db.create_all()
    from . import user
    app.register_blueprint(user.bp)
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app