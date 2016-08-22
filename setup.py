from setuptools import setup
from pip.req import parse_requirements
from hearcloud.settings import LOCAL_DEVELOPMENT, STAGING_ENVIRONMENT, PRODUCTION_ENVIRONMENT, TRAVIS_ENVIRONMENT

# parse_requirements() returns generator of pip.req.InstallRequirement objects
if LOCAL_DEVELOPMENT:
    install_reqs = parse_requirements('requirements/local.txt', session=False)
elif TRAVIS_ENVIRONMENT or STAGING_ENVIRONMENT:
    install_reqs = parse_requirements('requirements/staging.txt', session=False)
elif PRODUCTION_ENVIRONMENT:
    install_reqs = parse_requirements('requirements/production.txt', session=False)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(name='Hearcloud',
      version='0.1',
      description='Hearcloud',
      author='mpvillafranca',
      author_email='mpvillafranca@correo.ugr.es',
      url='http://github.com/mpvillafranca/hearcloud/',
      install_requires=reqs
     )
