#!/usr/bin/python
# WSGI openshift server config file
import os
import sys

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

os.environ['DJANGO_SETTINGS_MODULE'] = 'hearcloud.settings'

sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'])

from distutils.sysconfig import get_python_lib
os.environ['PYTHON_EGG_CACHE'] = get_python_lib()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


#def application(environ, start_response):
#
#    ctype = 'text/plain'
#    if environ['PATH_INFO'] == '/health':
#        response_body = "1"
#    elif environ['PATH_INFO'] == '/env':
#        response_body = ['%s: %s' % (key, value)
#                    for key, value in sorted(environ.items())]
#        response_body = '\n'.join(response_body)
        

#
# Below for testing only
#
#if __name__ == '__main__':
#    from wsgiref.simple_server import make_server
#    httpd = make_server('localhost', 8051, application)
#    # Wait for a single request, serve it and quit.
#    httpd.handle_request()
