# -*- coding:utf-8 -*-
from django.db import models


class NormalAccount(models.Model):
    GENDER = (
        (1,u"مرد"),
        (2,u"زن"),
    )
    cluster = models.ForeignKey("Cluster",verbose_name=u"خوشه",null=True,blank=True,related_name='members')
    picture = models.FileField(u"عکس")
    national_code = models.CharField(u"کد ملی",max_length=20)
    identification_number = models.CharField(u"شماره شناسنامه",max_length=20)
    phone = models.CharField(u"شماره تلفن",max_length=20)
    born_date = models.DateField(u"تاریخ تولد")
    city = models.CharField(u"شهر محل اقامت")
    gender = models.IntegerField(u'جنسیت',choices=GENDER)





class Cluster(models.Model):
    head = models.ForeignKey("NormalAccount",verbose_name=u"سرگروه خوشه")
    name = models.CharField(u"نام",max_length=200)


