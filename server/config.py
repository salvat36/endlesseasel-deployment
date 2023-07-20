# Standard library imports

# Remote library imports
from flask import Flask, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from os import environ
from dotenv import load_dotenv
import openai


# Local imports


# Instantiate app, set attributes
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)


load_dotenv(".env")
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
app.secret_key = environ.get("SECRET_KEY", "dev")
openai.api_key = environ.get('OPENAI_API_KEY', 'dev')

# Define metadata, instantiate db
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)

# Instantiate REST API
api = Api(app, prefix='/api')

# Instantiate CORS
CORS(app)

# Instantiate Bcrypt
bcrypt = Bcrypt(app)
