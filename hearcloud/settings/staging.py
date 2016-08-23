from .base import *
from . import STAGING_ENVIRONMENT, TRAVIS_ENVIRONMENT

DEBUG = False
ALLOWED_HOSTS = ['*']

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

if STAGING_ENVIRONMENT:
    import urlparse
    url = urlparse.urlparse(os.environ["OPENSHIFT_POSTGRESQL_DB_URL"])
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': url.path[1:],
		        'USER': url.username,
		        'PASSWORD': url.password,
		        'HOST': url.hostname,
		        'PORT': url.port,
        }
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

###############################################################################
"""                              CORS Headers                               """
""" https://github.com/ottoyiu/django-cors-headers                          """
###############################################################################
CORS_ORIGIN_ALLOW_ALL = True
