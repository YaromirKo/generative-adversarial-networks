from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), index=True)
    style = db.Column(db.Integer, index=True)

    def __init__(self, path, style):
        self.path = path
        self.style = style

    def __repr__(self):
        return '%s' % self.path
