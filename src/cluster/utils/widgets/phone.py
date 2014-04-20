# -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
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

        new_content = '/><span style="float:right;position: relative;top: 4px;left: 1px;">-</span>'.join(
            content.split('/>')[:3])
        new_content += content.split('/>')[-1:][0] + '/>'
        return mark_safe(before_content + new_content)


class EnglishPhoneNumberMultiWidget(PhoneNumberMultiWidget):
    def render(self, name, value, attrs=None):
        content = super(PhoneNumberMultiWidget, self).render(name, value, attrs)
        before_content = u'<span class="phone-example"> example : %s </span>' % self.example

        new_content = '/><span style="float:right;position: relative;top: 4px;left: 1px;">-</span>'.join(
            content.split('/>')[:3])
        new_content += content.split('/>')[-1:][0] + '/>'
        return mark_safe(before_content + new_content)



class MobileNumberMultiWidget(PhoneNumberMultiWidget):
    def __init__(self, attrs=None, example=None):
        self.example = example
        widgets = (
            forms.TextInput(
                attrs={'size': '7', 'maxlength': '7', 'class': 'phone',
                       'style': 'width: 80px !important; padding: 4px 2px;margin-left: 3px;'}),
            forms.TextInput(
                attrs={'size': '3', 'maxlength': '3', 'class': 'phone',
                       'style': 'width: 30px !important; padding: 4px 2px;margin-left: 3px;'}),
            forms.TextInput(
                attrs={'size': '2', 'maxlength': '2', 'class': 'phone',
                       'style': 'width: 30px !important;padding: 4px 2px;margin-left: 3px;'}),
        )
        super(PhoneNumberMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if value[0] == '0':
                value = value[1:]
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

class EnglishMobileNumberMultiWidget(MobileNumberMultiWidget):

    def render(self, name, value, attrs=None):
        content = super(PhoneNumberMultiWidget, self).render(name, value, attrs)
        before_content = u'<span class="phone-example"> example : %s </span>' % self.example

        new_content = '/><span style="float:right;position: relative;top: 4px;left: 1px;">-</span>'.join(
            content.split('/>')[:3])
        new_content += content.split('/>')[-1:][0] + '/>'
        return mark_safe(before_content + new_content)



class MobileNumberField(forms.CharField):

    def validate(self, value):
        super(MobileNumberField, self).validate(value)
        if value and len(value) != 14:
            raise ValidationError(u"شماره تلفن همراه باید 12 رقمی باشد.")

class EnglishMobileNumberField(forms.CharField):

    def validate(self, value):
        super(EnglishMobileNumberField, self).validate(value)
        if value and len(value) != 14:
            raise ValidationError(u"Mobile number should have 12 digits.")


def handle_phone_fields(form):
    from cluster.account.all_managers.international import InternationalAccountRegisterForm
    for field in form.fields:
        if field == 'telephone' or field == 'essential_telephone':
            form.fields[field].widget = PhoneNumberMultiWidget(example=u"87654321-21-98")
            if isinstance(form,InternationalAccountRegisterForm):
                form.fields[field].widget = EnglishPhoneNumberMultiWidget(example=u"98-21-7654321")

        elif field == 'mobile':
            old_label = form.fields[field].label
            old_required = form.fields[field].required
            old_initial = form.fields[field].initial
            form.fields[field] = MobileNumberField(label=old_label, required=old_required, initial=old_initial)
            form.fields[field].widget = MobileNumberMultiWidget(example=u"7654321-912-98")
            if isinstance(form,InternationalAccountRegisterForm):
                form.fields[field] = EnglishMobileNumberField(label=old_label, required=old_required, initial=old_initial)
                form.fields[field].widget = EnglishMobileNumberMultiWidget(example=u"98-912-7654321")
