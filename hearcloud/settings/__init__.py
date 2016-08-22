import os

LOCAL_DEVELOPMENT = True
STAGING_ENVIRONMENT = False
PRODUCTION_ENVIRONMENT = False
TRAVIS_ENVIRONMENT = False
#SNAP_CI_ENVIRONMENT = False


# Detecting environment by OS variables
if 'STAGING' in os.environ:
    LOCAL_DEVELOPMENT = False
    STAGING_ENVIRONMENT = True
elif 'PRODUCTION' in os.environ:
    LOCAL_DEVELOPMENT = False
    PRODUCTION_ENVIRONMENT = True
elif 'TRAVIS' in os.environ:
    LOCAL_DEVELOPMENT = False
    TRAVIS_ENVIRONMENT = True
#elif 'SNAP_CI' in os.environ:
#    LOCAL_DEVELOPMENT = False
#    SNAP_CI_ENVIRONMENT = True


# Choosing the correct settings
if LOCAL_DEVELOPMENT:
    from .local import *
elif TRAVIS_ENVIRONMENT:
    from .staging import *
    DATABASES = TRAVIS_DB
elif STAGING_ENVIRONMENT:
    from .staging import *
    DATABASES = OPENSHIFT_DB
elif PRODUCTION_ENVIRONMENT:
    from .production import *
