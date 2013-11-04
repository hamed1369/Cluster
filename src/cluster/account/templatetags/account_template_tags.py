# -*- coding:utf-8 -*-
import datetime
from django.contrib.auth.models import AnonymousUser
from cluster.utils.calverter import gregorian_to_jalali
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'
from django import template
from cluster import settings

register = template.Library()


@register.filter
def get_dict(input_dict, key):
    return input_dict.get(key)


@register.simple_tag
def welcome_st(user):
    if PermissionController.is_arbiter(user):
        overall_name = unicode(user.arbiter)
    else:
        overall_name = u"%s %s" % (user.first_name, user.last_name) if (
            user.first_name and user.last_name) else u"%s" % user.username
    return u"%s خوش آمدید." % overall_name


@register.filter
def is_false(value):
    return value is False or value == 'False'


@register.filter
def check_role(user, role_name):
    if isinstance(user, AnonymousUser):
        return False
    if role_name == 'member':
        return PermissionController.is_member(user)
    elif role_name == 'admin':
        return PermissionController.is_admin(user)
    elif role_name == 'arbiter':
        return PermissionController.is_arbiter(user)
    return False


@register.filter
def get_top_menus(user):
    return PermissionController.is_member(user)


@register.simple_tag(takes_context=True)
def render_url_li(context, url, persian_name):
    # url = reverse(name)
    html_class = 'active' if context.get('request').path == url else ''
    res = u"""
    <li>
        <a href="%s%s" class="%s">
            %s
        </a>
    </li>
    """ % (settings.SITE_URL, url, html_class, persian_name)
    return res


@register.simple_tag(takes_context=True)
def get_current_menu_name(context, menus):
    for menu in menus:
        if context.get('request').path == menu.url:
            return menu.show_name
    return u"صفحه اصلی"


@register.filter
def is_true(value):
    return value is True


@register.filter
def get_field(instance, name):
    return getattr(instance, name).all()


@register.filter
def pdate_if_date(value):
    if isinstance(value, datetime.date):
        return gregorian_to_jalali(value)
    if value is None or value == 'None' or value == '':
        return '---'
    return value


@register.filter
def show_m2m(value):
    return u', '.join([unicode(d) for d in value.all()])


@register.filter
def show_user_for_project_comments(user):
    if PermissionController.is_admin(user):
        return u"مدیر"
    elif PermissionController.is_arbiter(user):
        return u"داور"
    elif PermissionController.is_supervisor(user):
        return u"ناظر"
    else:
        return u"%s (متقاضی)" % unicode(user)


@register.filter
def is_admin(user):
    return PermissionController.is_admin(user)


@register.filter
def is_arbiter(user):
    return PermissionController.is_arbiter(user)


@register.filter
def filename(file_val):
    import os

    return os.path.basename(file_val.name)


@register.filter
def get_verbose_name_by_name(instance, name):
    return instance._meta.get_field_by_name(name)[0].verbose_name


