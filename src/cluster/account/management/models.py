# -*- coding:utf-8 -*-
from django.db import models
import os
from tinymce.models import HTMLField
__author__ = 'Hourshad'

def update_filename(instance, filename):
    path = "prop/sample_proposal.docx"
    return path
    #return os.path.join(path, 'sample_proposal.docx')

class IntroPageContent(models.Model):
    u"""
        محتوای صفحه اول
    """
    class Meta:
        verbose_name = u"محتوای صفحه اول"
        verbose_name_plural = u"محتوای صفحه اول"
        app_label = 'account'
    content = HTMLField(u"محتوای صفحه اول", max_length=5000)
    proposal_sample = models.FileField(u"نمونه پروپوزال", upload_to=update_filename,null=True,blank=False)

    instance = None

    @staticmethod
    def get_instance():
        if IntroPageContent.instance:
            return IntroPageContent.instance
        try:
            return IntroPageContent.objects.all()[0]
        except IndexError:
            return IntroPageContent.objects.create(content= " ")


    def save(self, force_insert=False, force_update=False, using=None):
        if self.pk:
            try:
                old_file = IntroPageContent.objects.get(pk=self.pk).proposal_sample
            except IntroPageContent.DoesNotExist:
                return False
            if old_file:
                new_file = self.proposal_sample
                if not old_file == new_file:
                    if os.path.isfile(old_file.path):
                        os.remove(old_file.path)
        return super(IntroPageContent,self).save(force_insert, force_update, using)
