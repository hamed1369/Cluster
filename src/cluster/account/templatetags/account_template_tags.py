# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse

__author__ = 'M.Y'
from django import template
from cluster import settings

register = template.Library()


@register.filter
def get_dict(input_dict, key):
    return input_dict.get(key)


@register.simple_tag
def welcome_st(user):
    overall_name = u"%s %s" % (user.first_name, user.last_name) if (
        user.first_name and user.last_name) else u"%s" % user.username
    return u"%s خوش آمدید." % overall_name


@register.filter
def is_false(value):
    return value is False or value == 'False'


@register.simple_tag(takes_context=True)
def render_url_li(context, name, persian_name):
    url = reverse(name)
    html_class = 'active' if context.get('request').path.startswith(url) else ''
    res = u"""
    <li>
        <a href="%s%s" class="%s">
            %s
        </a>
    </li>
    """ % (settings.SITE_URL, url, html_class, persian_name)
    return res