from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path_input_img  = db.Column(db.String(100), index=True)
    path_target_img = db.Column(db.String(100), index=True)
    style = db.Column(db.Integer, index=True)

    def __init__(self, path_input_img, path_target_img, style):
        self.path_input_img = path_input_img
        self.path_target_img = path_target_img
        self.style = style
    #
    # def __repr__(self):
    #     return self.path_input_img, self.path_target_img
