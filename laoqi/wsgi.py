"""
WSGI config for laoqi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/rmd/PycharmProjects/loaqi/laoqiVenv/lib/python3.6/site-packages')
sys.path.append('/home/rmd/PycharmProjects/loaqi')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laoqi.settings')

application = get_wsgi_application()
