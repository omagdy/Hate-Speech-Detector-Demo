import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "mail.fim.uni-passau.de"
    MAIL_PORT = os.environ.get('MAIL_PORT') or 25
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or "offdet.no-reply@uni-passau.de"
    MAIL_RECEIVER = os.environ.get('MAIL_RECEIVER') or "hussei05@ads.uni-passau.de"
    MAIL_USE_TLS = 0
    MAIL_PASSWORD=""

