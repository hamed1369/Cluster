# -*- coding: utf-8 -*-
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
