
class Config:

    # Flask
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'overpoweredsecretkey'


    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
