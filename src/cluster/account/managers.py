# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from cluster.utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'

class UserManager(ObjectsManager):
    manager_name = u"users"
    manager__verbose_name = u"کاربران"

    def get_all_data(self):
        return User.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('username', u"نام کاربری", 'auto')
        ]
        return columns
