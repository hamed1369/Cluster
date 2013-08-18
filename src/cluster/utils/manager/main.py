# -*- coding: utf-8 -*-
__author__ = 'M.Y'

manager_children = []


class ManagerRegister(type):
    def __new__(mcs, name, bases, classdict):
        new_cls = type.__new__(mcs, name, bases, classdict)
        if not new_cls in manager_children:
            manager_children.append(new_cls)
        return new_cls


class ObjectsManager(object):
    __metaclass__ = ManagerRegister

    manager_name = ""
    manager_verbose_name = ""

    def __init__(self, http_request):
        self.http_request = http_request

    def get_all_data(self):
        """
            این تابع باید داده ها را برای لیست کردن برگرداند
        """
        return []

    def get_columns(self):
        columns = [
            # list of ManagerColumn
        ]
        return columns

    def can_view(self):
        """
            این تابع چک میکند که کاربر میتواند این صفحه را ببیند یا خیر
        """
        return True


class ManagerColumn(object):
    def __init__(self, column_name, column_verbose_name, column_width):
        self.column_name = column_name
        self.column_verbose_name = column_verbose_name
        self.column_width = column_width