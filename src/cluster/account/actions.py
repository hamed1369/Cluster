# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from cluster.utils.manager.action import ManagerAction

__author__ = 'M.Y'


class DeleteUserAction(ManagerAction):
    action_name = 'delete_user'
    action_verbose_name = u"حذف کاربر"

    def do(self, http_request, selected_instances):
        for user in selected_instances:
            user.delete()


class ChangeUserName(ManagerAction):
    action_name = 'change_user_name'
    action_verbose_name = u"تغییر نام"
    is_view = True

    def action_view(self, http_request, selected_instances):
        return render_to_response()
