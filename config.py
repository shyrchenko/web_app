class Config:
    POSTS_PER_PAGE = 5


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://master:master_password@localhost:3306/app_db'
    SQLALCHEMY_ECHO = False


class ProdConfig(Config):
    pass

