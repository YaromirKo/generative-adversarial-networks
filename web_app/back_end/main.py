from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

CORS(app)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), index=True)
    style = db.Column(db.Integer, index=True)

    def __init__(self, path, style):
        self.path = path
        self.style = style

    def __repr__(self):
        return '%s' % self.path


@app.route('/')
def user():
    return jsonify(user=456)


@app.route('/api')
def test():
    return jsonify('s')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files
    return jsonify(file_name=file)
    # img = Image("path_test_2", 10)
    # db.session.add(img)
    # db.session.commit()


@app.route('/get')
def get():
    path_list = Image.query.filter_by(style=10).limit(10).all()
    # path_json = {'path{}'.format(k): v for k, v in enumerate(path_list)}

    return jsonify(path=[i.path for i in path_list])


if __name__ == '__main__':
    app.run(debug=True)
