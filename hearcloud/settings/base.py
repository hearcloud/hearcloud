###############################################################################
"""                     HEARCLOUD project settings file                     """
"""                                   with Django 1.9.5                     """
"""                                                                         """
"""                 For more information on this file, see:                 """
"""          https://docs.djangoproject.com/en/1.9/topics/settings/         """
###############################################################################

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
DJANGO_APPS = [
    'suit',  # Admin theme
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'easy_pjax',
    'crispy_forms',
    'fm',
    'easy_thumbnails',
  
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
]

LOCAL_APPS = [
    'applications.box',
    'applications.users',
    'applications.home',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

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


###############################################################################
"""                               Django Suit                               """
""" http://django-suit.readthedocs.io/                                      """
###############################################################################
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Hearcloud',
    # 'HEADER_DATE_FORMAT': 'l, j. F Y',
    # 'HEADER_TIME_FORMAT': 'H:i',

    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    # 'MENU_ICONS': {
    #    'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    'MENU': (
        'sites',
        {'app': 'auth', 'icon':'icon-lock', 'models': (AUTH_USER_MODEL, 'group')},
        {'app': 'box', 'icon': 'icon-cog', 'models': ('song', 'playlist')},
        #{'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
        #{'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    ),

    # misc
    # 'LIST_PER_PAGE': 15
}


###############################################################################
"""                              Rest Framework                             """
""" http://www.django-rest-framework.org/                                   """
###############################################################################
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
     ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'PAGE_SIZE': 10
}


###############################################################################
"""                            Rest Auth/All auth                           """
""" http://django-rest-auth.readthedocs.io/                                 """
###############################################################################
SITE_ID = 1

EMAIL_BACKEND= 'django.core.mail.backends.console.EmailBackend'
