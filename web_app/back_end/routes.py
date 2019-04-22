import os

from flask import jsonify, request
from app import *


@app.route('/')
def user():
    return jsonify(user=456)


@app.route('/api')
def test():
    return jsonify('s')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.getlist("file")
    for file in file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return jsonify(data="success")
    # img = Image("path_test_2", 10)
    # db.session.add(img)
    # db.session.commit()


@app.route('/get')
def get():
    path_list = Image.query.filter_by(style=10).limit(10).all()
    # my_list = []
    #
    # for i in path_list:
    #     my_list.append({i.path: i.id})
    return jsonify(path=[i.path for i in path_list])
