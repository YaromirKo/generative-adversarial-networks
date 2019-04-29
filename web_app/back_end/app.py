from flask_cors import CORS
from flask import Flask
from models import *

app = Flask(__name__)

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, resources={r"/*": {"origins": OROGINS}})

db.init_app(app)

# if DB_INIT:
#     app.app_context().push()
#     db.create_all()
