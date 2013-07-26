# -*- coding:utf-8 -*-
from khooshe.account.account.models import Member
from django.db import models

class EducationalResume(models.Model):

    EDUCATIONAL_STATUS = (
        (1,u"دانشجو"),
        (2,u"فارغ التحصیل")
        )
    SECTIONS =(
        (1,u"کاردانی"),
        (2,u"کارشناسی"),
        (3,u"کارشناسی ارشد"),
        (4,u"دکتری")
        )
    educational_status  = models.IntegerField(u"وضعیت تحصیلی",choices=EDUCATIONAL_STATUS )
    section             = models.IntegerField(u"مقطع تحصیلی",choices=SECTIONS)
    institution         = models.CharField(u"نام محل تحصیل", max_length=30)
    field               = models.CharField(u"رشته", max_length=25)
    orientation         = models.CharField(u"گرایش", max_length=25)
    average             = models.FloatField(u"معدل")
    start_year          = models.IntegerField(u"سال شروع")
    end_year            = models.IntegerField(u"سال پایان")
    country             = models.CharField(u"کشور", max_length=20)
    city                = models.CharField(u"شهر", max_length=20)
    cluster_member = models.ForeignKey(Member,related_name="educational_resumes")

    class Meta:
        app_label ='account'
        verbose_name = u"رزومه تحصیلی"
        verbose_name_plural =u"رزومه های تحصیلی"

class Publication(models.Model):
    title               = models.CharField(u"عنوان", max_length=300)
    authors             = models.CharField(u"نویسنده / نویسندگان", max_length=400)
    date                = models.DateField(u"تاریخ چاپ/ برگزاری همایش")
    journal_conference_name = models.CharField(u"عنوان نشریه/ همایش", max_length=300)
    organizer           = models.CharField(u"انتشارات/ برگزار کنندگان همایش", max_length=300)
    cluster_member = models.ForeignKey(Member,related_name="publications")

    class Meta:
        app_label ='account'
        verbose_name = u"مقاله پژوهشی/کتاب چاپ شده"
        verbose_name_plural = u"مقالات پژوهشی/ کتاب های چاپ شده"

    def __unicode__(self):
        return unicode(self.title)

class Invention(models.Model):
    title               = models.CharField(u"عنوان اختراع", max_length=300)
    registration_number = models.CharField(u"شماره ثبت", max_length=25) # احتمالا کاراکتر هم دارد پس char در نظر گرفته شد
    registration_date   = models.DateField(u"تاریخ ثبت")
    participation       = models.IntegerField(u"درصد مشارکت")
    cluster_member = models.ForeignKey(Member,related_name="inventions")

    class Meta:
        app_label ='account'
        verbose_name = u"اختراع"
        verbose_name_plural = u"اختراعات"

class ExecutiveResearchProject(models.Model):
    title       = models.CharField(u"عنوان", max_length=300)
    author      = models.CharField(u"مجری / نویسنده", max_length=400)
    start_date  = models.DateField(u"تاریخ شروع")
    end_date    = models.DateField(u"تاریخ پایان")
    place       = models.CharField(u"محل اجرا", max_length=200)
    cluster_member = models.ForeignKey(Member,related_name="executive_research_projects")

    class Meta:
        verbose_name = u"اجرایی یا طرح پژوهشی"
        verbose_name_plural = u"اجرایی ها یا طرح های پژوهشی"

class LanguageSkill(models.Model):
    STATUS = (
        (1,u"تسلط کامل"),
        (2,u"متوسط"),
        (3,u"ضعیف")
        )
    language    = models.CharField(u"زبان", max_length=30)
    read        = models.IntegerField(u"خواندن", choices=STATUS)
    write       = models.IntegerField(u"نوشتن", choices=STATUS)
    listening   = models.IntegerField(u"شنیدن", choices=STATUS)
    cluster_member = models.ForeignKey(Member,related_name="language_skills")

    class Meta:
        app_label ='account'
        verbose_name = u"مهارت زبان"
        verbose_name_plural = u"مهارت های زبان"

class SoftwareSkill(models.Model):
    STATUS = (
        (1,u"تسلط کامل"),
        (2,u"آشنایی"),
        (3,u"مبتدی")
        )

    software    = models.CharField(u"نرم افزار", max_length=30)
    status      = models.IntegerField(u"سطح مهارت", choices=STATUS)
    cluster_member = models.ForeignKey(Member,related_name="software_skills")

    class Meta:
        app_label ='account'
        verbose_name = u"مهارت نرم افزاری"
        verbose_name_plural = u"مهارت های نرم افزاری"
