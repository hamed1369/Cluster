# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import transaction
from cluster.account.account.models import Cluster
from cluster.account.personal_info.models import EducationalResume, SoftwareSkill, LanguageSkill, \
    ExecutiveResearchProject, Invention, Publication
from cluster.project.forms import ProjectForm
from cluster.project.models import Domain
from cluster.registration.forms import ClusterForm, RegisterForm, ClusterMemberForm, ClusterDomainForm, ResumeForm, \
    PublicationForm, InventionForm, ExecutiveResearchProjectForm, LanguageSkillForm, SoftwareSkillForm
from cluster.utils.messages import MessageServices

__author__ = 'M.Y'


class ProjectHandler(object):
    def __init__(self, http_request):
        self.http_request = http_request
        self.http_method = self.http_request.method

    def initial_forms(self, check_post=True):
        if self.http_request.method == 'POST' and self.http_request.POST.get('register-submit') and check_post:
            self.register_form = ProjectForm(self.http_request.POST, prefix='project')
        else:
            self.register_form = ProjectForm(prefix='project')

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
