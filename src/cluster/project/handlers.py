# -*- coding:utf-8 -*-
from django.db import transaction
from cluster.project.forms import ProjectForm

__author__ = 'M.Y'


class ProjectHandler(object):
    def __init__(self, http_request):
        self.http_request = http_request
        self.http_method = self.http_request.method

    def initial_forms(self, check_post=True):
        if self.http_request.method == 'POST' and self.http_request.POST.get('register-submit') and check_post:
            self.register_form = ProjectForm(self.http_request.POST, self.http_request.FILES, prefix='project',
                                             user=self.http_request.user)
        else:
            self.register_form = ProjectForm(prefix='project', user=self.http_request.user)

    def is_valid_forms(self):
        validate = False
        if self.register_form.is_valid():
            validate = True
        return validate

    @transaction.commit_on_success
    def save_forms(self):
        self.register_form.save()

    def get_context(self):
        c = {
            'register_form': self.register_form
        }
        return c
