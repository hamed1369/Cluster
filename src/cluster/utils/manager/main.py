# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.context import RequestContext
from django.template.loader import render_to_string
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

    def render_main_list(self):
        self.columns = self.get_columns()
        c = {
            'manager': self
        }
        main_list_content = render_to_string('manager/main_list.html', c,
                                             context_instance=RequestContext(self.http_request))
        return main_list_content

    def process_action_request(self):
        all_data = self.get_all_data()
        filter_obj = Filter(all_data, self.http_request, self.filter_form, self.filter_handlers, self.data_per_page)
        filter_form, page_data = filter_obj.process_filter()
        table = self._create_data_table(page_data)
        json = table.get_dgrid_json(filter_obj.total_pages, filter_obj.page_num, filter_obj.total_data)
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



