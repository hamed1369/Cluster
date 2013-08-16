# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
from cluster.utils.calverter import jalali_to_gregorian, gregorian_to_jalali

__author__ = 'M.Y'
from django import forms


class ShamsiWidget(forms.DateInput):
    def render(self, name, value, attrs=None):
        value = gregorian_to_jalali(value)
        html = super(ShamsiWidget, self).render(name, value, attrs)
        js = """
        <script type='text/javascript'>
            $('#id_%s').datepicker({
                changeMonth: true,
                changeYear: true,
                dateFormat: 'yy/mm/dd'
            });
        </script>
        """ % name
        return mark_safe(u"%s %s" % (html, js))

    def value_from_datadict(self, data, files, name):
        shamsi_val = data.get(name, None)
        miladi_val = jalali_to_gregorian(shamsi_val)
        return miladi_val.isoformat()


class ShamsiDateField(forms.DateField):
    widget = ShamsiWidget

    def to_python(self, value):
        return super(ShamsiDateField, self).to_python(value)


