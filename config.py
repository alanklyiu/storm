import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Put any configurations here that are common across all environments
    pass

class DevelopmentConfig(Config):
    #DEBUG = True
    #SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

class ProductionConfig(Config):
    #DEBUG = False
    pass

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}