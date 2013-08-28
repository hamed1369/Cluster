# -*- coding: utf-8 -*-
from django.conf import settings

__author__ = 'M.Y'


def register_children():
    for app in settings.INSTALLED_APPS:
        try:
            __import__(app + '.managers')
        except ImportError:
            pass