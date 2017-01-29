"""
WSGI config for preeclampsia_db project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "preeclampsia_db.settings")

application = get_wsgi_application()


# def application(environ, start_response):
#     if environ['mod_wsgi.process_group'] != '': 
#         import signal
#         os.kill(os.getpid(), signal.SIGINT)
#     return [b"killed"]

# def application(environ, start_response):
#     status = '200 OK'
#     output = b'Hello World!'

#     response_headers = [('Content-type', 'text/plain'),
#                         ('Content-Length', str(len(output)))]
#     start_response(status, response_headers)

#     return [output]