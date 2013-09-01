# -*- coding: utf-8 -*-
__author__ = 'M.Y'


class ManagerAction(object):
    action_name = u""  # the name that use for creating js and ajax
    action_verbose_name = u""  # the name that show to user
    is_view = False  # if True should override action_view

    def do(self, http_request, selected_instances):
        pass

    def action_view(self, http_request, selected_instances):
        pass