class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///wibed.db"
    SECRET_KEY = "WIBED"
    OVERLAY_DIR = "static/overlays"
    FIRMWARE_DIR = "static/firmwares"

class ProductionConfig(Config):
    SECRET_KEY = "<PUT A BIG KEY HERE>"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"

