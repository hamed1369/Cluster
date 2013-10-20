# -*- coding:utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

__author__ = 'M.Y'


class PhoneNumberMultiWidget(forms.MultiWidget):
    def __init__(self, attrs=None, example=None):
        self.example = example
        widgets = (
            forms.TextInput(
                attrs={'size': '8', 'maxlength': '8', 'class': 'phone',
                       'style': 'width: 80px !important; padding: 4px 2px;margin-left: 3px;'}),
            forms.TextInput(
                attrs={'size': '3', 'maxlength': '3', 'class': 'phone',
                       'style': 'width: 30px !important; padding: 4px 2px;margin-left: 3px;'}),
            forms.TextInput(
                attrs={'size': '3', 'maxlength': '3', 'class': 'phone',
                       'style': 'width: 30px !important;padding: 4px 2px;margin-left: 3px;'}),
        )
        super(PhoneNumberMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            values = value.split('-')
            if len(values) == 3:
                return [values[2], values[1], values[0]]
            return [value[6:], value[3:6], value[:3]]
        return tuple([None, None, None])

    def value_from_datadict(self, data, files, name):
        value = [u'', u'', u'']
        for d in filter(lambda x: x.startswith(name), data):
            index = int(d[len(name) + 1:])
            value[index] = data[d]
        if value[0] == value[1] == value[2] == u'':
            return None
        value = list(reversed(value))
        return u'%s-%s-%s' % tuple(value)

    def render(self, name, value, attrs=None):
        content = super(PhoneNumberMultiWidget, self).render(name, value, attrs)
        before_content = u'<span class="phone-sign">+</span><span class="phone-example"> مثال : %s </span>' % self.example
        return mark_safe(before_content + content)


def handle_phone_fields(form):
    for field in form.fields:
        if field == 'telephone' or field == 'essential_telephone':
            form.fields[field].widget = PhoneNumberMultiWidget(example=u"87654321 21 98")
            #elif field == 'mobile':
            #    form.fields[field].widget = PhoneNumberMultiWidget(example=u"456789 123 912")
