# -*- coding:utf-8 -*-
from cluster.utils.fields.date_fields import ShamsiDateField

__author__ = 'M.Y'
from django import forms


def handel_date_fields(form):
    for field in form.fields:
        if isinstance(form.fields[field], (forms.DateField, forms.DateTimeField)):
            old_field = form.fields[field]
            new_field = ShamsiDateField(label=old_field.label, required=old_field.required, initial=old_field.initial)
            form.fields[field] = new_field

