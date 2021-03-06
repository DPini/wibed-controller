class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///wibed.db"
    SECRET_KEY = "WIBED"
    OVERLAY_DIR = "static/overlays"
    FIRMWARE_DIR = "static/firmwares"
    RESULTS_DIR = "static/results"
    ERROR_DIR = "static/error"
    JS_DIR = "static/js"
    LOG_DIR = "log"
    REACHABLE_WINDOW = 180 ## number of seconds after which a node that hasn't
                           ## made contact is shown as unreachable

class ProductionConfig(Config):
    SECRET_KEY = "<PUT A BIG KEY HERE>"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    REACHABLE_WINDOW = 1
