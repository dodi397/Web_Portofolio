from datetime import datetime

from .extensions import db


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False, default='Nama Mahasiswa')
    headline = db.Column(db.String(160), nullable=False, default='Web Developer & Problem Solver')
    about = db.Column(db.Text, nullable=False, default='')
    photo_file = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), nullable=False, default='email@example.com')
    github_link = db.Column(db.String(255), nullable=True)
    linkedin_link = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    education_title_1 = db.Column(db.String(120), default='Pengantar Pemrograman')
    education_desc_1 = db.Column(db.Text, default='Belajar Python, Flask, SQLite, Jinja2, routing, form handling, dan deployment dasar.')
    education_title_2 = db.Column(db.String(120), default='Pengembangan Web')
    education_desc_2 = db.Column(db.Text, default='Belajar UI modern, komponen responsif, dan struktur project yang rapi untuk presentasi akademik.')

    skills = db.relationship('Skill', backref='profile', cascade='all, delete-orphan', lazy=True)
    educations = db.relationship('Education', backref='profile', cascade='all, delete-orphan', lazy=True)


class Education(db.Model):
    __tablename__ = 'educations'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=80)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(255), nullable=False, default='')
    image_file = db.Column(db.String(255), nullable=True)
    github_link = db.Column(db.String(255), nullable=True)
    live_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def tech_items(self):
        return [item.strip() for item in (self.technologies or '').split(',') if item.strip()]


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
