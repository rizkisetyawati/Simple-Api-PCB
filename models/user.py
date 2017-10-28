from datetime import datetime
from uuid import uuid1
from core.db import db

# model tabel member
class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    id_pub = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    mobile_phone = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), default=('L', 'P'), nullable=False)
    about = db.Column(db.String(150))
    interest = db.Column(db.String(150))
    semester = db.Column(db.String(2), default=('1', '2', '3', '4'), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    mentor = db.Column(db.Boolean, default=False)
    articles = db.relationship('Article', backref='user', lazy=True)
    events = db.relationship('Event', backref='user', lazy=True)
    megazines = db.relationship('Megazine', backref='user', lazy=True)
    date_register = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, first_name, last_name, password, email, mobile_phone, gender, about, interest, semester):
        self.id_pub = "member-"+str(uuid1())
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.mobile_phone = mobile_phone
        self.gender = gender
        self.about = about
        self.interest = interest
        self.semester = semester

    @classmethod
    def find_by_id(cls, id_pub):
        return cls.query.filter_by(id_pub=id_pub).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, mobile_phone):
        return cls.query.filter_by(mobile_phone=mobile_phone).first()

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
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'mobile_phone': self.mobile_phone,
                'admin': self.admin,
                'gender': self.gender,
                'about': self.about,
                'interest': self.interest,
                'date_register': str(self.date_register),
                'semester': self.semester}

    # di gunakan untuk debug
    def __repr__(self):
        return ('name {} {}'.format(self.first_name, self.last_name))
