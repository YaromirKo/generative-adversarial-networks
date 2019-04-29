from flask import jsonify, request
from app import *
from pix2pix import Pix2Pix
import zipfile


@app.route('/upload', methods=['GET', 'POST'])
def upload():

    global zip_path, zip_file
    target_img_path = ' '
    if request.method == 'POST':
        generator = Pix2Pix()
        id_style = request.form["id_style"]
        generator.set_weight(str(id_style))
        files = request.files.getlist('file')
        if len(files) > 1:
            zip_path = './static/' + files[0].filename + 'style.zip'
            zip_file = zipfile.ZipFile(zip_path, 'w')
        for file in files:
            if PRODUCTION:
                input_img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(input_img_path)
                target_img_path = generator.predict(input_img_path)
                img = Image(path_input_img=input_img_path, path_target_img=target_img_path, style=id_style)
                if len(files) > 1:
                    zip_file.write(target_img_path)
                db.session.add(img)
        db.session.commit()
        if len(files) > 1:
            target_img_path = zip_path
            zip_file.close()
    return jsonify(link=target_img_path[1:])


@app.route('/get_paths', methods=['GET'])
def get():
    id_style = request.args.get('id_style')
    path_list = Image.query.filter_by(style=id_style).limit(10).all()
    path = []
    for i in path_list:
        path.append({
            'path_input': i.path_input_img[1:],
            'path_target': i.path_target_img[1:]
        })
    return jsonify(path=[i for i in path])


@app.route('/delete', methods=['DELETE'])
def delete_data():
    Image.query.delete()
    for i in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, i)
        os.unlink(file_path)
    db.session.commit()
    return jsonify(data="success")
