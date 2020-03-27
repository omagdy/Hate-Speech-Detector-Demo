import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MAIL_SERVER = "mail.fim.uni-passau.de"
    MAIL_PORT = 25
    MAIL_USE_TLS = 0
    MAIL_PASSWORD=""
    MAIL_DEFAULT_SENDER="offdet.no-reply@uni-passau.de"

