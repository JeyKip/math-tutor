from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['PG_DATABASE_NAME'],
        'USER': os.environ['PG_DATABASE_USER'],
        'PASSWORD': os.environ['PG_DATABASE_PASSWORD'],
        'HOST': os.environ['PG_DATABASE_HOST'],
        'PORT': os.environ['PG_DATABASE_PORT'],
    }
}
