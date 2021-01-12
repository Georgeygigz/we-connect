import os
import sys
from pathlib import Path  # python3 only

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)


class Config():
    DEBUG = False
    TOKEN_EXP_TIME = os.getenv("TOKEN_EXP_TIME", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery configuration
    REDIS_URL = os.getenv('REDIS_URL', default='redis://localhost:6379/0')
    CELERYD_POOL_RESTARTS = True
    CELERY_BROKER_URL = os.getenv(
        'CELERY_BROKER_URL', default='redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv(
        'CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
    VERIFY_URL = os.getenv('VERIFY_URL', '')

    # email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', '')
    MAIL_PORT = os.getenv('MAIL_PORT', '')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', '')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', '')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    AUTH_URL = '/api/v1/users/'
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
    FLASK_ENV = 'testing'


app_configuration = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}

AppConfig = TestingConfig if 'pytest' in sys.modules else app_configuration.get(os.getenv('FLASK_ENV', 'development'))
