from .base import *
from . import PRODUCTION_ENVIRONMENT
from ansible_vault import Vault

vault = Vault(os.environ['VAULT_PASSWORD'])
passwords = vault.load(open(os.path.join(BASE_DIR, 'vars.yml')).read())
print passwords

DEBUG = False
ALLOWED_HOSTS = ['*']

###############################################################################
"""                                Database                                 """
""" https://docs.djangoproject.com/en/1.9/ref/settings/#databases           """
###############################################################################

if PRODUCTION_ENVIRONMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['MYSQL_DB'],
            'USER': 'root',
            'PASSWORD': os.environ['MYSQL_PASS'],
            'HOST': 'localhost',
            'PORT': '3307',
        }
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join('/var/www/', STATIC_URL.strip("/"))
MEDIA_ROOT = os.path.join('/var/www/', MEDIA_URL.strip("/"))

###############################################################################
"""                              CORS Headers                               """
""" https://github.com/ottoyiu/django-cors-headers                          """
###############################################################################
CORS_ORIGIN_ALLOW_ALL = True
