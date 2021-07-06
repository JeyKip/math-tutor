from .base import *

INTERNAL_IPS = [
    '127.0.0.1', '::1', 'localhost'
]

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

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
