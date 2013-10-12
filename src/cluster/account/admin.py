# -*- coding:utf-8 -*-
from django.contrib import admin
from cluster.account.account.models import Member, Arbiter, Cluster, Domain
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill

__author__ = 'M.Y'

admin.site.register(Member)
admin.site.register(Arbiter)
admin.site.register(Cluster)
admin.site.register(EducationalResume)
admin.site.register(Publication)
admin.site.register(Invention)
admin.site.register(ExecutiveResearchProject)
admin.site.register(LanguageSkill)
admin.site.register(SoftwareSkill)
admin.site.register(Domain)
