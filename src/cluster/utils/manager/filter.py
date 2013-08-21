# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from cluster.utils.calverter import jalali_to_gregorian

__author__ = 'M.Y'


class Filter(object):
    def __init__(self, all_data, http_request, filter_form, filter_handlers, data_per_page):
        self.all_data = all_data
        self.http_request = http_request
        self.page_num = self.http_request.GET.get('page') or 1
        self.filter_form = filter_form
        self.filter_handlers = filter_handlers
        self.data_per_page = data_per_page

    def process_filter(self):
        kwargs = {}
        form = None
        if self.filter_form:
            form = self.filter_form(self.http_request.GET)
            form_data = form.data
            for handler in self.filter_handlers:
                field_name = handler[0]
                field_type = handler[1]
                django_lookup = handler[2] or field_name
                field_value = form_data.get(field_name)
                if field_value and field_value != 'None':
                    if field_type == 'str':
                        kwargs[django_lookup + 'icontains'] = field_value
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
        all_data = self.all_data.filter(**kwargs)

        p = Paginator(all_data, self.data_per_page)
        self.total_pages = p.num_pages
        self.total_data = p.count
        page = p.page(self.page_num)
        paginate_data = page.object_list

        return form, paginate_data







