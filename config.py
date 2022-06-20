class Config:
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://master:master_password@localhost:3306/app_db'
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    pass

