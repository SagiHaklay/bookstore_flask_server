from datetime import timedelta

SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:Mysqlpassword42!@localhost/bookstore"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
JWT_SECRET_KEY = 'SuPeRsEcReTkEy!!1'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
UPLOAD_FOLDER = "C://projects/talpiot/TalpiotBookstore/bookstore_flask_server/flaskr/static"