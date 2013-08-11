# -*- coding:utf-8 -*-
from django.contrib import admin
from cluster.project.models import Project, Domain

__author__ = 'M.Y'

admin.site.register(Project)
admin.site.register(Domain)
