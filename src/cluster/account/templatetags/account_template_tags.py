# -*- coding:utf-8 -*-
__author__ = 'M.Y'
from django import template

register = template.Library()


@register.filter
def get_dict(input_dict, key):
    return input_dict.get(key)


@register.simple_tag
def welcome_st(user):
    return u"%s %s عزیز،<br/> خوش آمدید" % (user.first_name, user.last_name)