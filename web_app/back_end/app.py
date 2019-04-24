from flask_cors import CORS, cross_origin
from flask import Flask
from models import *
from config import *


app = Flask(__name__)

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, resources={r"/*": {"origins": OROGINS}})

# CORS(app)

db.init_app(app)
