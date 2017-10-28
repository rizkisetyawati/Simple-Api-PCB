from datetime import datetime
from uuid import uuid1
from core.db import db

# model tabel megazine
class Megazine(db.Model):
    # __tablename__ = 'megazine'

    id = db.Column(db.Integer, primary_key=True)
    id_pub = db.Column(db.String(150), unique=True)
    id_author = db.Column(db.String(150), db.ForeignKey('user.id_pub'))
    title = db.Column(db.String(40))
    about = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, id_author, title, about):
        self.id_pub = 'megazine-' + str(uuid1())
        self.id_author = id_author
        self.title = title
        self.about = about

    @classmethod
    def find_by_id(cls, id_pub):
        return cls.query.filter_by(id_pub=id_pub).first()

    @classmethod
    def find_by_author(cls, id_author):
        return cls.query.filter_by(id_author=id_author).first()

    # simpan
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # hapus
    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id_pub': self.id_pub,
                'id_author': self.id_author,
                'title': self.title,
                'about': self.about,
                'timestamp': str(self.timestamp)}

    # di gunakan untuk debug
    def __repr__(self):
        return ('title {}'.format(self.title))
