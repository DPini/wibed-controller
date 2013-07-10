class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///wibed.db"
    SECRET_KEY = "WIBED"

class ProductionConfig(Config):
    SECRET_KEY = "<PUT A BIG KEY HERE>"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
