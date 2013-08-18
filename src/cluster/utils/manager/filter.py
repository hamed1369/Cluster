# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from cluster.utils.calverter import jalali_to_gregorian

__author__ = 'M.Y'


class Filter(object):
    filter_form = None
    data_per_page = 20

    filter_handlers = (
        ()
        # ('name_of_field', 'type_of_field', 'django_lookup')
        # type_of_field = str|bool|m2o|m2m|pdate
    )

    def __init__(self, all_data, http_request, page_num):
        self.all_data = all_data
        self.http_request = http_request
        self.page_num = page_num

    def process_filter(self):
        form = self.filter_form(self.http_request.GET)
        form_data = form.data
        kwargs = {}
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
        page = p.page(self.page_num)
        paginate_data = page.object_list

        return form, paginate_data







