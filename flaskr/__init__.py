import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flaskr.database import db

# UPLOAD_FOLDER = '/static'

def create_app():
    app = Flask(__name__)
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:Adht7244!@localhost:3306/bookstore"
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    app.config.from_object('flaskr.default_settings')
    app.config.from_envvar('APPLICATION_SETTINGS')
    jwt = JWTManager(app)
    CORS(app)
    db.init_app(app)
    import flaskr.models
    with app.app_context():
        db.create_all()
    from . import user
    app.register_blueprint(user.bp)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import product
    app.register_blueprint(product.bp)
    from . import cart
    app.register_blueprint(cart.bp)
    
    return app