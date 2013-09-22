# -*- coding: utf-8 -*-
from django.db import models
from cluster.account.account.models import Member, Cluster, Domain


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
    STATUS = (
        (-1,u"رد شده"),
        (0,u"در مرحله درخواست"),
        (1,u"تایید مرحله اول"),
        (2,u"تایید مرحله دوم"),

    )
    title               = models.CharField(u"عنوان طرح", max_length=300)
    confirmation_type   = models.IntegerField(u"تاییدیه علمی و نوآوری", choices=CONFIRM_TYPE, default=1)
    certificate_image   = models.FileField(u"تصویر مدرک تاییدیه", upload_to="project_certificate_images/", null=True, blank=True)
    has_patent          = models.BooleanField(u"دارای ثبت اختراع", default=False)
    patent_number       = models.CharField(u"شماره ثبت اختراع", max_length=20, null=True, blank=True)
    patent_date         = models.DateField(u"تاریخ ثبت اختراع", null=True, blank=True)
    patent_certificate  = models.FileField(u"مدرک ثبت اختراع", upload_to="project_patents/", null=True, blank=True)
    patent_request      = models.BooleanField(u"تقاضای ثبت اختراع", default=False)
    domain              = models.ForeignKey(Domain, verbose_name=u"حوزه علمی و کاربردی طرح", related_name='projects', on_delete=models.SET_NULL, null=True)
    summary             = models.CharField(u"خلاصه طرح", max_length=2000)
    keywords            = models.CharField(u"کلید واژه", max_length=100)
    innovations         = models.CharField(u"نوآوری های طرح" , max_length=300)
    state               = models.IntegerField(u"مرحله", choices=STATE)
    project_status      = models.IntegerField(u"مرحله داوری", choices=STATUS, default=0)

    single_member       = models.ForeignKey(Member,verbose_name=u"عضو", null=True, blank=True)
    cluster             = models.ForeignKey(Cluster, verbose_name=u"خوشه", null=True, blank=True)

    class Meta:
        verbose_name = u"طرح"
        verbose_name_plural = u"طرح ها"


class ProjectMilestone(models.Model):
    created_on = models.DateField(verbose_name=u"تاریخ ایجاد", auto_now_add=True)
    comment = models.CharField(verbose_name=u"توضیح", max_length=200)
    project = models.ForeignKey(Project, verbose_name=u"طرح")

    class Meta:
        verbose_name = u"مرحله موعد"
        verbose_name_plural = u"مراحل موعد"


