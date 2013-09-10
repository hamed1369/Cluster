# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import Q
from cluster.account.account.models import Arbiter, Member

__author__ = 'M.Y'


class PermissionController:
    @classmethod
    def is_admin(cls, user):
        if user.is_superuser:
            return True
        if user.groups.filter(name=u"مدیر"):
            return True
        return False

    @classmethod
    def is_arbiter(cls, user):
        try:
            Arbiter.objects.get(user=user)
            return True
        except Arbiter.DoesNotExist:
            return False

    @classmethod
    def is_member(cls, user):
        try:
            Member.objects.get(user=user)
            return True
        except Member.DoesNotExist:
            return False

    @classmethod
    def get_admins(cls):
        query = Q(is_superuser=True) | Q(groups__name=u"مدیر")
        return User.objects.filter(query)

    @classmethod
    def get_available_receivers(cls, user):
        if cls.is_admin(user):
            return User.objects.filter()
        elif cls.is_arbiter(user):
            return cls.get_admins()
        elif cls.is_member(user):
            return user.member.cluster.users.filter()
        else:
            return User.objects.none()


    @classmethod
    def get_user_menus(cls, user):
        if user.is_anonymous():
            return []
        elif cls.is_admin(user):
            return MENU_MAPPERS['admin']
        elif cls.is_arbiter(user):
            return MENU_MAPPERS['arbiter']
        elif cls.is_member(user):
            return MENU_MAPPERS['member']
        else:
            return []


class MenuMapper:
    def __init__(self, url, show_name):
        self.url = url
        self.show_name = show_name


MENU_MAPPERS = {
    'admin': [
        MenuMapper('/manager/domains/', u"مدیریت حوزه ها"),
        MenuMapper('/accounts/edit/', u"ویرایش اطلاعات فردی"),
        MenuMapper('/manager/users/', u"مدیریت کاربران"),
        MenuMapper('/manager/clusters/', u"مدیریت خوشه ها"),
        MenuMapper('/manager/messages/', u"جعبه پیام"),
    ],
    'arbiter': [
        MenuMapper('/', u"صفحه اصلی"),
        MenuMapper('/arbiter_edit/', u"ویرایش اطلاعات فردی"),
        MenuMapper('/manager/projects/', u"بررسی طرح ها"),
        MenuMapper('/manager/messages/', u"جعبه پیام"),
    ],
    'member': [
        MenuMapper('/', u"صفحه اصلی"),
        MenuMapper('/accounts/edit/', u"ویرایش اطلاعات فردی"),
        MenuMapper('/manager/confirmed_inventions/', u"مشاهده اختراعات تاییدشده"),
        MenuMapper('/manager/messages/', u"جعبه پیام"),
    ]
}