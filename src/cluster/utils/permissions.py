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
