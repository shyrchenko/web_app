from main import app, db, User, Post, Tag, Comment, migrate


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, Comment=Comment, migrate=migrate)

