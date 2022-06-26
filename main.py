from flask import Flask, render_template, redirect, request
from flask_migrate import Migrate
from config import DevConfig
from utils import TypedSQLAlchemy
import datetime
import uuid
import hashlib
from sqlalchemy import func, desc
from typing import Optional, Tuple


app = Flask(__name__)
app.config.from_object(DevConfig)

db = TypedSQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime(), default=datetime.datetime.now())
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __init__(self, username: str, password: str):
        self.id = str(uuid.uuid4())
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
    id = db.Column(db.String(255), primary_key=True)
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
        self.id = str(uuid.uuid4())
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)


class Comment(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.now())
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.String(255), db.ForeignKey('post.id'), nullable=False)

    def __init__(self, text):
        self.id = str(uuid.uuid4())
        self.text = text

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])


class Tag(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    def __init__(self, title):
        self.id = str(uuid.uuid4())
        self.title = title


def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(tags).group_by(Tag).order_by(desc('total')).limit(5).all()
    return recent, top_tags


@app.template_filter('none_to_str')
def none_to_str(text: Optional[str]) -> str:
    if text is None:
        return ''
    else:
        return text


@app.route('/')
@app.route('/<int:page>')
def home(page: int = 1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    recent, top_tags = sidebar_data()

    return render_template(
        'posts.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@app.route('/post/<string:post_id>')
def post(post_id: str):
    post_object = Post.query.filter(Post.id == post_id).one()
    recent, top_tags = sidebar_data()
    comments_with_users: Tuple[Comment, User] = db.session.query(
        Comment, User).filter(Comment.post_id == post_id).join(User, Comment.user_id == User.id).all()

    return render_template(
        'post.html',
        post=post_object,
        recent=recent,
        comments_with_users=comments_with_users,
        top_tags=top_tags
    )


@app.post('/comment')
def add_comment():
    text = request.form.get('text')
    post_id = request.form.get('post_id')
    comment = Comment(text)
    comment.user_id = '1a0e5a8e-37df-4a09-88d7-29275a36ab1a'
    comment.post_id = post_id
    db.session.add(comment)
    db.session.commit()
    return redirect(f'/post/{post_id}')


if __name__ == '__main__':
    app.run()
