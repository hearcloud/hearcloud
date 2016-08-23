from .base import *
from . import LOCAL_DEVELOPMENT

DEBUG = True
ALLOWED_HOSTS = []

###############################################################################
"""                                Database                                 """
""" https://docs.djangoproject.com/en/1.9/ref/settings/#databases           """
###############################################################################

if LOCAL_DEVELOPMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
