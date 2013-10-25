# -*- coding:utf-8 -*-
'''
Created on 21/07/13

@author: hamed
'''

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cluster',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


SECRET_KEY = 'local!'

BASE_PATH = 'D:/Documents/Aptana/Khooshe'
SITE_URL = 'localhost:8000'
MEDIA_ROOT = BASE_PATH+'media/'
STATIC_ROOT = BASE_PATH+'static/'
STATICFILES_DIRS = (
    STATIC_ROOT,
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
)