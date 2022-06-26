from main import db, User, Post, Tag
import pandas as pd

df = pd.read_csv('./blogtext.csv')

user_id = User.query.first().id

for _, row in df.sample(100).iterrows():
    text = row['text']
    if len(text) < 100:
        continue
    title = " ".join(row['text'].split()[:6]) + "..."

    tag_title = row['topic']
    if Tag.query.filter(Tag.title == tag_title).count() == 0:
        tag_object = Tag(tag_title)
        db.session.add(tag_object)
        db.session.commit()

    tag = Tag.query.filter(Tag.title == tag_title).first()
    post = Post(title)
    post.text = text
    post.user_id = user_id
    post.tags.append(tag)
    db.session.add(post)
    db.session.commit()

