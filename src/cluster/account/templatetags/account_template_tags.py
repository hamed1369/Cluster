# -*- coding:utf-8 -*-
__author__ = 'M.Y'
from django import template

register = template.Library()


@register.filter
def get_dict(input_dict, key):
    return input_dict.get(key)