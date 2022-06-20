from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from typing import Callable


_flask_sqlalchemy_annotations = {}
for module in sqlalchemy, sqlalchemy.orm:
    for key in module.__all__:
        _flask_sqlalchemy_annotations[key] = Callable

TypedSQLAlchemy = type('TypedSQLAlchemy', (SQLAlchemy, ), {'__annotations__': _flask_sqlalchemy_annotations})
