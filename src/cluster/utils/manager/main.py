# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.utils.manager.filter import Filter
from cluster.utils.manager.table import Table, Header, Row

__author__ = 'M.Y'

manager_children = []


class ManagerRegister(type):
    def __new__(mcs, name, bases, classdict):
        new_cls = type.__new__(mcs, name, bases, classdict)
        if not new_cls in manager_children:
            manager_children.append(new_cls)
        return new_cls


class ManagerColumn(object):
    def __init__(self, column_name, column_verbose_name, column_width):
        self.column_name = column_name
        self.column_verbose_name = column_verbose_name
        self.column_width = column_width


class ObjectsManager(object):
    __metaclass__ = ManagerRegister

    manager_name = ""
    manager_verbose_name = ""
    filter_form = None
    filter_handlers = (
        ()
        # ('name_of_field', 'type_of_field', 'django_lookup')
        # type_of_field = str|bool|m2o|m2m|pdate
    )
    data_per_page = 20

    actions = []

    def __init__(self, http_request):
        self.http_request = http_request
        self.columns = self.get_columns()
        self.filter_obj = Filter(self.http_request, self.filter_form, self.filter_handlers, self.data_per_page)
        all_data = self.get_all_data()
        self.filter_form, self.page_data = self.filter_obj.process_filter(all_data)

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

    def render_main_list(self):
        if not self.can_view():
            raise Http404()
        c = {
            'manager': self
        }
        return render_to_response('manager/main.html', c, context_instance=RequestContext(self.http_request))

    def process_action_request(self):
        table = self._create_data_table(self.page_data)
        json = table.get_dgrid_json(self.filter_obj.total_pages, self.filter_obj.page_num, self.filter_obj.total_data)
        return HttpResponse(json, mimetype='application/json')

    def _create_data_table(self, page_data):
        id_columns = ManagerColumn('id', 'id', '0')
        columns = [id_columns] + self.get_columns()
        table = Table()
        header = Header()
        for column in columns:
            header.create_cell(column.column_name, column.column_verbose_name, column.column_width)

        table.set_header(header)
        for data in page_data:
            row = Row()
            for column in columns:
                value = getattr(data, column.column_name)
                row.create_cell(column.column_name, unicode(value), column.column_width)
            table.add_row(row)
        return table
