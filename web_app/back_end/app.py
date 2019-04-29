from flask_cors import CORS
from flask import Flask
from models import *
from config import *

app = Flask(__name__)

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

CORS(app, resources={r"/*": {"origins": OROGINS}})


db.init_app(app)

if DB_INIT:
    app.app_context().push()
    db.create_all()
