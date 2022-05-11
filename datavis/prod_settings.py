import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '8gk+lpagp&c1$-gciv73jfdd=-e&y@jk7m=69irygou+3r2hp'

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "92.53.105.244"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'postgress',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}