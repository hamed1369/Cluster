# -*- coding: utf-8 -*-
from django.db import models

class Project(models.Model):
    CONFIRM_TYPE=(
        (1,u"ندارد"),
        (2,u"تاییدیه سازمان پژوهش های علمی و صنعتی ایران"),
        (3,u"برگزیده جشنواره خوارزمی"),
        (4,u"برگزیده جشنواره رازی"),
        (5,u"برگزیده جشنواره شیخ بهائی"),
        (6,u"برگزیده جشنواره فارابی"),
        (7,u"سایر دانشگاه ها و مراکز دولتی"),
    )
    STATE = (
        (1,u"ایده"),
        (2,u"مدل و ماکت و تکمیل پژوهش"),
        (3,u"نمونه آزمایشی"),
        (4,u"در حال تولید"),
    )
    title               = models.CharField(u"عنوان طرح", max_length=300)
    confirmation_type   = models.IntegerField(u"تاییدیه علمی و نوآوری", choices=CONFIRM_TYPE, default=1)
    certificate_image   = models.FileField(u"تصویر مدرک تاییدیه", upload_to="project_certificate_images/", null=True, blank=True)
    has_patent          = models.BooleanField(u"دارای ثبت اختراع", default=False)
    patent_number       = models.CharField(u"شماره ثبت اختراع", max_length=20, null=True, blank=True)
    patent_date         = models.DateField(u"تاریخ ثبت اختراع", null=True, blank=True)
    patent_certificate  = models.FileField(u"مدرک ثبت اختراع", upload_to="project_patents/", null=True, blank=True)
    patent_request      = models.BooleanField(u"تقاضای ثبت اختراع", default=False)
    domain              = models.ForeignKey('Domain',verbose_name=u"حوزه علمی و کاربردی طرح", related_name='projects')
    summary             = models.CharField(u"خلاصه طرح", max_length=2000)
    keywords            = models.CharField(u"کلید واژه", max_length=100)
    innovations         = models.CharField(u"نوآوری های طرح" , max_length=300)
    state               = models.IntegerField(u"مرحله", choices=STATE)


    class Meta:
        verbose_name = u"طرح"
        verbose_name_plural = u"طرح ها"

class Domain(models.Model):
    name = models.CharField(u"نام حوزه", max_length=40)
    confirmed = models.BooleanField(u"تایید شده", default=False)

    class Meta:
        verbose_name = u"حوزه"
        verbose_name_plural = u"حوزه ها"

    def __unicode__(self):
        if not self.confirmed:
            return unicode(self.name)+u"(تایید نشده)"
        else:
            return unicode(self.name)
