from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)


@app.route('/')
def user():
    return jsonify(user=456)


if __name__ == '__main__':
    app.run(debug=True)
