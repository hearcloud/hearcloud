###############################################################################
"""                     HEARCLOUD project settings file                     """
"""                                   with Django 1.9.5                     """
"""                                                                         """
"""                 For more information on this file, see:                 """
"""          https://docs.djangoproject.com/en/1.9/topics/settings/         """
###############################################################################

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#PROJECT_ROOT = os.path.dirname(__file__)
#sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b%sv-2nk)(cidk1&n1=9y$m#jz36!5hn18*12=tsyvu&(_$j5)'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []



###############################################################################
"""                         Application definition                          """
###############################################################################
INSTALLED_APPS = [
    # Core:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party:
    'corsheaders',
    'rest_framework',
    'easy_pjax',
    'crispy_forms',
    'fm',
    'easy_thumbnails',

    # Project:
    'box',
    'users',
    'home',
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hearcloud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': [
                'easy_pjax.templatetags.pjax_tags'
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hearcloud.wsgi.application'

###############################################################################
"""                                Database                                 """
""" https://docs.djangoproject.com/en/1.9/ref/settings/#databases           """
###############################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


###############################################################################
"""                              CORS Headers                               """
""" https://github.com/ottoyiu/django-cors-headers                          """
###############################################################################
CORS_ORIGIN_ALLOW_ALL = True



###############################################################################
"""                            Custom user model                            """
###############################################################################
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/login/'



###############################################################################
"""                           Dual Authentication                           """
""" https://pypi.python.org/pypi/django-dual-authentication/1.0.0           """
###############################################################################
AUTHENTICATION_BACKENDS = ['django-dual-authentication.backends.DualAuthentication']

# Options: username, email, both
# Default: both
AUTHENTICATION_METHOD = 'both'

# Options: username, email, both, none
# Default: both
AUTHENTICATION_CASE_SENSITIVE = 'both'
