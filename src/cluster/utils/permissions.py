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
            return user.member.cluster.user_domains.filter().values_list('user', flat=True)
        else:
            return User.objects.none()


    @classmethod
    def get_user_menus(cls, user):
        perms = []
        if user.is_anonymous():
            return []
        if cls.is_admin(user):
            perms = perms + MENU_MAPPERS['admin']
        if cls.is_arbiter(user):
            perms = perms + MENU_MAPPERS['arbiter']
        if cls.is_member(user):
            perms = perms + MENU_MAPPERS['member']

        return perms

    @classmethod
    def get_user_redirect_url(cls, user):
        if cls.is_admin(user):
            return MENU_MAPPERS['admin'][0].url
        elif cls.is_arbiter(user):
            return MENU_MAPPERS['arbiter'][1].url
        elif cls.is_member(user):
            return MENU_MAPPERS['member'][1].url
        return '/'


class MenuMapper:
    def __init__(self, url, show_name):
        self.url = url
        self.show_name = show_name

    def __eq__(self, other):
        if other.url == self.url:
            return True


MENU_MAPPERS = {
    'admin': [
        MenuMapper('/domains/', u"مدیریت حوزه ها"),
        MenuMapper('/accounts/edit/', u"ویرایش اطلاعات فردی"),
        MenuMapper('/members/', u"مدیریت افراد"),
        MenuMapper('/clusters/', u"مدیریت خوشه ها"),
        MenuMapper('/messages/', u"جعبه پیام"),
    ],
    'arbiter': [
        MenuMapper('/', u"صفحه اصلی"),
        MenuMapper('/arbiter_edit/', u"ویرایش اطلاعات فردی"),
        MenuMapper('/projects/', u"بررسی طرح ها"),
        MenuMapper('/messages/', u"جعبه پیام"),
    ],
    'member': [
        MenuMapper('/', u"صفحه اصلی"),
        MenuMapper('/accounts/edit/', u"ویرایش اطلاعات فردی"),
        MenuMapper('/confirmed_inventions/', u"مشاهده اختراعات تاییدشده"),
        MenuMapper('/messages/', u"جعبه پیام"),
    ]
}