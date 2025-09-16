import os

from flask import Flask
from flaskr.database import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:Adht7244!@localhost:3306/bookstore"
    db.init_app(app)
    import flaskr.models
    with app.app_context():
        db.create_all()
    from . import user
    app.register_blueprint(user.bp)
    return app