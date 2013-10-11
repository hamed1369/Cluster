# -*- coding:utf-8 -*-
'''
Created on 04/10/13

@author: hamed
'''

from django.core.management.base import NoArgsCommand
from cluster.project.models import ProjectMilestone

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        ProjectMilestone.check_milestones()
