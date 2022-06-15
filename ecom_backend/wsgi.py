"""
WSGI config for ecom_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_backend.settings')

import socketio
from notifications.views import sio

django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)

import eventlet.wsgi
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
