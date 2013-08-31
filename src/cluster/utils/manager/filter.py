# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from cluster.utils.calverter import jalali_to_gregorian

__author__ = 'M.Y'


class Filter(object):
    def __init__(self, http_request, filter_form, filter_handlers, data_per_page):
        self.http_request = http_request
        self.page_num = self.http_request.GET.get('page') or 1
        self.filter_form = filter_form
        self.filter_handlers = filter_handlers
        self.data_per_page = data_per_page
        self.ordering_handle()

    def process_filter(self, all_data):
        kwargs = {}
        form = None
        if self.filter_form:
            form = self.filter_form(self.http_request.GET)
            form_data = form.data
            for handler in self.filter_handlers:
                field_name = handler[0]
                field_type = handler[1]

                if len(handler) > 2:
                    django_lookup = handler[2] or field_name
                else:
                    django_lookup = field_name

                field_value = form_data.get(field_name)
                if field_value and field_value != 'None':
                    if field_type == 'str':
                        kwargs[django_lookup + '__icontains'] = field_value
                    elif field_type == 'bool':
                        if field_value == 'on':
                            kwargs[django_lookup] = True
                    elif field_type == 'm2o':
                        kwargs[django_lookup + '__id'] = field_value
                    elif field_type == 'm2m':
                        kwargs[django_lookup + '__in'] = field_value
                    elif field_type == 'pdate':
                        miladi_date = jalali_to_gregorian(field_value).isoformat()
                        kwargs[django_lookup] = miladi_date
                    else:
                        kwargs[django_lookup] = field_value
        all_data = all_data.filter(**kwargs).order_by(self.order_field)

        p = Paginator(all_data, self.data_per_page)
        self.total_pages = p.num_pages
        self.total_data = p.count
        page = p.page(self.page_num)
        paginate_data = page.object_list

        return form, paginate_data

    def ordering_handle(self):
        self.order_field = 'id'
        order_field = self.http_request.GET.get('sidx')
        order_type = self.http_request.GET.get('sord')
        if order_field:
            if order_type == 'asc':
                self.order_field = order_field
            else:
                self.order_field = '-' + order_field
