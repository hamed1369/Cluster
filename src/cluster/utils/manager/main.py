# -*- coding: utf-8 -*-
from datetime import date
from django.db import models
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.html import strip_tags
from django.utils.safestring import SafeUnicode, SafeString
from cluster.utils.calverter import gregorian_to_jalali
from cluster.utils.manager.filter import Filter
from cluster.utils.manager.table import Table, Header, Row
from django.template import Template, Context

__author__ = 'M.Y'

manager_children = []


class ManagerRegister(type):
    def __new__(mcs, name, bases, classdict):
        from cluster.urls import urlpatterns
        from django.conf.urls import patterns, url

        new_cls = type.__new__(mcs, name, bases, classdict)
        if not new_cls in manager_children:
            manager_children.append(new_cls)
            urlpatterns += patterns('cluster.utils.manager.views',
                                    url(r'^%s/$' % new_cls.manager_name, 'process_main_page',
                                        {'manager_name': new_cls.manager_name}),
                                    url(r'^%s/actions/$' % new_cls.manager_name, 'process_actions',
                                        {'manager_name': new_cls.manager_name}),
            )
        return new_cls


class ManagerColumn(object):
    def __init__(self, column_name, column_verbose_name, column_width, is_variable=False, allow_html=False,
                 aggregation=False):
        self.column_name = column_name
        self.column_verbose_name = column_verbose_name
        self.column_width = column_width
        self.is_variable = is_variable
        self.allow_html = allow_html
        self.aggregation = aggregation


class ManagerGroupHeader(object):
    def __init__(self, start_column_name, number_column, title):
        self.start_column_name = start_column_name
        self.number_column = number_column
        self.title = title


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
    data_per_page = 10
    aggregation = False

    actions = []

    # view quality attributes
    height = 310

    def __init__(self, http_request):
        self.http_request = http_request
        self.columns = self.get_columns()
        rows = http_request.GET.get('rows') or self.data_per_page
        self.filter_obj = Filter(self.http_request, self.filter_form, self.filter_handlers, rows)
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
        action_type = self.http_request.GET.get('t')
        if action_type == 'json':
            return self.process_json()
        elif action_type == 'action':
            return self.process_manages_actions()
        elif action_type == 'excel':
            return self.process_excel()
        raise Http404()

    def process_json(self):
        table = self._create_data_table(self.page_data)
        json = table.get_dgrid_json(self.filter_obj.total_pages, self.filter_obj.page_num, self.filter_obj.total_data,
                                    self.aggregation)
        return HttpResponse(json, mimetype='application/json')

    def process_manages_actions(self):
        action_name = self.http_request.GET.get('n')
        instances_id = self.http_request.GET.get('i')
        selected_instances = self._get_instances_by_ids(instances_id)
        for action in self.actions:
            if action.action_name == action_name:
                if action.is_view:
                    return action.action_view(self.http_request, selected_instances)
                else:
                    action.do(self.http_request, selected_instances)
                    return HttpResponse('OK')
        raise Http404()

    def _create_data_table(self, page_data, columns=None):
        id_columns = ManagerColumn('id', 'id', '0')
        if not columns:
            columns = [id_columns] + self.get_columns()
        table = Table()
        header = Header()
        for column in columns:
            header.create_cell(column.column_name, column.column_verbose_name, column.column_width, column.aggregation)

        table.set_header(header)
        for data in page_data:
            row = Row()
            for column in columns:
                if column.is_variable:
                    function = getattr(self, 'get_' + column.column_name)
                    value = function(data)
                else:
                    value = getattr(data, column.column_name)
                if isinstance(value, bool):
                    if value is True:
                        value = u"بله"
                    else:
                        value = u"خیر"
                elif isinstance(value, date):
                    value = gregorian_to_jalali(value)
                elif isinstance(data, models.Model) and not column.is_variable:
                    if data.__class__._meta.get_field_by_name(column.column_name)[0].choices:
                        value = getattr(data, 'get_' + column.column_name + '_display')()
                if not isinstance(value, (SafeUnicode, SafeString)):
                    value = unicode(value)
                if value is None or value == 'None':
                    value = u"---"
                row.create_cell(column.column_name, value, column.column_width, column.aggregation)
            table.add_row(row)
        return table

    def get_filter_form_content(self):
        return None

    def get_compiled_filter_form_content(self):
        content = self.get_filter_form_content()
        return Template(content).render(Context({'form': self.filter_form}))

    def _get_instances_by_ids(self, instances_id):
        if instances_id:
            try:
                instances_id = [int(x) for x in instances_id.split(',')]
            except ValueError:
                return []
            instances = []
            all_data = self.get_all_data()
            for data in all_data:
                if data.id in instances_id:
                    instances.append(data)
            return instances
        return []

    def process_excel(self):
        import xlsxwriter
        import string

        try:
            import cStringIO as StringIO
        except ImportError:
            import StringIO

        columns = self.get_excel_columns()
        table = self._create_data_table(self.filter_obj.all_data, columns)

        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        worksheet.right_to_left()

        bold = workbook.add_format({'bold': True})
        i = 1
        letters = string.uppercase
        for cell in table.header:
            column_head = letters[i - 1]
            worksheet.set_column(column_head + ':' + column_head, int(cell.width) * 2)
            worksheet.write_string(0, i - 1, strip_tags(cell.value), bold)
            i += 1

        row_i = 1
        align_format = workbook.add_format({'align': 'right'})
        for row in table:
            cell_i = 0
            for cell in row:
                worksheet.write_string(row_i, cell_i, strip_tags(cell.value), align_format)
                cell_i += 1
            row_i += 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=%s.xlsx" % self.manager_name

        return response

    def get_excel_columns(self):
        return []

    def get_group_headers(self):
        return []