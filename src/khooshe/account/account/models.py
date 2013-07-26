# -*- coding:utf-8 -*-
from khooshe.project.models import Domain

__author__ = 'Hourshad'
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    GENDER = (
        (1,u"مرد"),
        (2,u"زن")
        )
    gender          = models.IntegerField(u"جنسیت", choices=GENDER)
    father_name     = models.CharField(u"نام پدر", max_length=30)
    national_code   = models.BigIntegerField(u"کد ملی")
    identification_number = models.BigIntegerField(u"شماره شناسنامه")
    birth_date      = models.DateField(u"تاریخ تولد")
    residence_city  = models.CharField(u"شهر محل اقامت", max_length=20)
    telephone       = models.CharField(u"تلفن ثابت", max_length=15)
    mobile          = models.CharField(u"تلفن همراه", max_length=11)
    essential_telephone = models.CharField(u"تلفن ضروری", max_length=15)
    address         = models.CharField(u"آدرس", max_length=400)
    class Meta:
        abstract = True

class Member(Account):

    EMPLOYMENT_STATUS =(
        (1,u"شاغل"),
        (2,u"دانشجو"),
        )
    MILITARY_STATUS =(
        (1,u"دارای کارت پایان خدمت"),
        (2,u"در حال خدمت"),
        (3,u"دارای کارت معافیت"),
        )
    EXEMPTION=(
        (1,u"معافیت تحصیلی"),
        (2,u"معافیت دائم")
    )
    cluster             = models.ForeignKey('Cluster',related_name="members", null=True, blank=True)
    user                = models.OneToOneField(User,related_name = "member")
    employment_status   = models.IntegerField(u"وضعیت شغلی", choices=EMPLOYMENT_STATUS)
    organization        = models.CharField(u"محل کار", max_length=30, null=True, blank=True)
    military_status     = models.IntegerField(u"وضعیت نظام وظیفه",choices=MILITARY_STATUS )
    military_place      = models.CharField(u"محل خدمت", max_length=30, null=True, blank=True)
    exemption_type      = models.IntegerField(u"نوع معافیت",choices=EXEMPTION, null=True, blank=True)
    foundation_of_elites = models.BooleanField(u"عضویت در بنیاد ملی نخبگان", default=False)
    image               = models.FileField(u"عکس", upload_to="member_images/", null=True, blank=True)
    elite_certification = models.FileField(u"مدرک نخبگی", upload_to="elite_certificates/", null=True, blank=True)
    front_id_card       = models.FileField(u"تصویر روی کارت ملی", upload_to="national_id_cards/", null=True,blank=True)
    back_id_card        = models.FileField(u"تصویر پشت کارت ملی", upload_to="national_id_cards/", null=True, blank=True)
    education_certification = models.FileField(u"تصویر آخرین مدرک تحصیلی", upload_to="education_certificates", null=True, blank=True)

    class Meta:
        app_label ='account'
        verbose_name = u"عضو خوشه"
        verbose_name_plural =u"اعضای خوشه"


class Arbiter(Account):
    user            = models.OneToOneField(User,related_name = "arbiter")
    workplace       = models.CharField(u"نام محل کار", max_length=30)
    field           = models.CharField(u"رشته", max_length=20)
    professional    = models.CharField(u"گرایش تخصصی", max_length=20)
    degree          = models.CharField(u"مرتبه علمی", max_length=20) # TODO : ابهام
    office_phone    = models.CharField(u"تلفن مخل کار" , max_length=15)
    fax             = models.CharField(u"فکس", max_length=15)
    interested_domain = models.ManyToManyField(Domain,related_name="arbiters",verbose_name=u"حوزه مورد علاقه")

    class Meta:
        app_label ='account'
        verbose_name = u"داور"
        verbose_name_plural =u"داورها"

class Cluster(models.Model):
    name        = models.CharField(u"نام خوشه", max_length=50)
    domains     = models.ManyToManyField(Domain,related_name='clusters',verbose_name=u"حوزه فعالیت",) # TODO : ابهام
    institute   = models.CharField(u"دانشگاه / موسسه", max_length=30)
    head        = models.OneToOneField(Member,verbose_name=u"سر خوشه",related_name='head_cluster')

    class Meta:
        app_label ='account'
        verbose_name = u"خوشه"
        verbose_name_plural =u"خوشه ها"