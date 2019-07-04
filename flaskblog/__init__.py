#  Package structure, where app will initialize
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# Flask used to create app
# SQLAlchemy for database


app = Flask(__name__)


# used for protection (ex: cookie modification)
# token generated using secrets.token_hex()
app.config['SECRET_KEY'] = '7fec327b7e1da6f8b90966f78d7372d1'
# /// indicates relative path, where the sb will be stored
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Getting the db
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# initialize routes
from flaskblog import routes