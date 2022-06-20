from flask import Flask
from flask_migrate import Migrate
from config import DevConfig
from utils import TypedSQLAlchemy
import datetime
import uuid
import hashlib


app = Flask(__name__)
app.config.from_object(DevConfig)

db = TypedSQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime(), default=datetime.datetime.now())
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __init__(self, username: str, password: str):
        self.username = username
        self.hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    def __repr__(self):
        return f'User {self.username}'


tags = db.Table(
    'post_tags',
    db.Column('tag_id', db.String(255), db.ForeignKey('tag.id')),
    db.Column('post_id', db.String(255), db.ForeignKey('post.id'))
)


class Post(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime(), default=datetime.datetime.now())
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='posts', lazy='dynamic')
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)


class Comment(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=str(uuid.uuid4()))
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.now())
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.String(255), db.ForeignKey('post.id'), nullable=False)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])


class Tag(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)

    def __init__(self, title):
        self.title = title


@app.route('/')
def main():
    return '<h1>Hello world</h1>'


if __name__ == '__main__':
    app.run()
