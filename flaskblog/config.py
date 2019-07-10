import os

class Config:
    # used for protection (ex: cookie modification), token generated using secrets.token_hex()
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # /// indicates relative path, where the sb will be stored
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # setup mail server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    # Using user set environmental vars to ensure info not in code
    MAIL_USERNAME = os.environ.get('MAIL_EMAIL')
    MAIL_PASSWORD = os.environ.get('MAIL_PASS')
