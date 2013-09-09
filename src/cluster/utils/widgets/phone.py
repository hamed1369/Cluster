from django import forms
from django.utils.safestring import mark_safe

__author__ = 'M.Y'


class PhoneNumberMultiWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(
                attrs={'size': '8', 'maxlength': '8', 'class': 'phone',
                       'style': 'width: 80px; padding: 4px 2px;margin-left: 3px;'}),
            forms.TextInput(
                attrs={'size': '3', 'maxlength': '3', 'class': 'phone',
                       'style': 'width: 30px; padding: 4px 2px;margin-left: 3px;'}),
            forms.TextInput(
                attrs={'size': '3', 'maxlength': '3', 'class': 'phone',
                       'style': 'width: 30px;padding: 4px 2px;margin-left: 3px;'}),
        )
        super(PhoneNumberMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value[:3], value[3:6], value[6:]]
        return tuple([None, None, None])

    def value_from_datadict(self, data, files, name):
        value = [u'', u'', u'']
        for d in filter(lambda x: x.startswith(name), data):
            index = int(d[len(name) + 1:])
            value[index] = data[d]
        if value[0] == value[1] == value[2] == u'':
            return None
        value = list(reversed(value))
        return u'%s%s%s' % tuple(value)

    def render(self, name, value, attrs=None):
        content = super(PhoneNumberMultiWidget, self).render(name, value, attrs)
        return mark_safe(u'<span class="phone-sign">+</span>' + content)


def handle_phone_fields(form):
    for field in form.fields:
        if field == 'telephone':
            form.fields[field].widget = PhoneNumberMultiWidget()
