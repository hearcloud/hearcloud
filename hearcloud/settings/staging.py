from .base import *
from . import STAGING_ENVIRONMENT, TRAVIS_ENVIRONMENT

DEBUG = False
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

###############################################################################
"""                                Database                                 """
""" https://docs.djangoproject.com/en/1.9/ref/settings/#databases           """
###############################################################################

if TRAVIS_ENVIRONMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travisdb',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip("/"))
    MEDIA_ROOT = os.path.join(BASE_DIR, *MEDIA_URL.strip("/").split("/"))


if STAGING_ENVIRONMENT:
    import urlparse
    url = urlparse.urlparse(os.environ["OPENSHIFT_POSTGRESQL_DB_URL"])
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['OPENSHIFT_APP_NAME'],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        }
    }
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')


###############################################################################
"""                              CORS Headers                               """
""" https://github.com/ottoyiu/django-cors-headers                          """
###############################################################################
CORS_ORIGIN_ALLOW_ALL = True
