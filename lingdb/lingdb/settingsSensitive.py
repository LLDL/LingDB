from lingdb.common import *

SECRET_KEY = ""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lingdev',
        'USER': 'lingtechpg',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
