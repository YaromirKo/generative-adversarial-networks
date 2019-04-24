from flask import jsonify, request
from app import *


@app.route('/')
def user():
    return jsonify(user=456)


@app.route('/api')
def test():
    return jsonify('s')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    id_style = request.form['id_style']
    file = request.files.getlist("file")

    for file in file:
        if PRODUCTION:
            path_file = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path_file)
            img = Image(path=path_file, style=id_style)
            db.session.add(img)

    db.session.commit()

    return jsonify(data="success")


@app.route('/get')
def get():
    path_list = Image.query.filter_by(style=10).limit(10).all()
    # my_list = []
    #
    # for i in path_list:
    #     my_list.append({i.path: i.id})
    return jsonify(path=[i.path for i in path_list])
