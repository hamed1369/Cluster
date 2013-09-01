# -*- coding:utf-8 -*-
from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User
from cluster.account.account.models import Member
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill
from cluster.project.models import Domain, Project
from cluster.utils.forms import ClusterBaseForm, ClusterBaseModelForm
from cluster.utils.js_validation import process_js_validations

__author__ = 'M.Y'


class ProjectForm(ClusterBaseModelForm):
    class Meta:
        model = Project

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = super(ProjectForm, self).clean()
        return cd

