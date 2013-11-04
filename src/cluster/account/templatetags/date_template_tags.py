# -*- coding: utf-8 -*-
import datetime
from cluster.utils.calverter import Calverter, JALALI_WEEKDAYS

__author__ = 'Hourshad'

from django import template

register = template.Library()

@register.filter
def persian_date(date):
    date_converter = Calverter()
    jd = date_converter.gregorian_to_jd(date.year, date.month, date.day)
    sh_date = date_converter.jd_to_jalali(jd)
    week_day = date_converter.jwday(jd)
    day_name = JALALI_WEEKDAYS[week_day]
    st = str(sh_date[0])+"/"+str(sh_date[1])+"/"+str(sh_date[2])
    return u"امروز، %s %s"%(day_name,st)

@register.filter
def pdate(date):
    date_converter = Calverter()
    jd = date_converter.gregorian_to_jd(date.year, date.month, date.day)
    sh_date = date_converter.jd_to_jalali(jd)
    st = str(sh_date[0])+"/"+str(sh_date[1])+"/"+str(sh_date[2])
    return u"%s"%st

@register.simple_tag
def get_current_date_time():
    date = datetime.datetime.now()
    date_converter = Calverter()
    jd = date_converter.gregorian_to_jd(date.year, date.month, date.day)
    sh_date = date_converter.jd_to_jalali(jd)
    week_day = date_converter.jwday(jd)
    day_name = JALALI_WEEKDAYS[week_day]
    st = str(sh_date[0])+"/"+str(sh_date[1])+"/"+str(sh_date[2])
    return u"اکنون، %s %s ساعت %s و %s دقیقه"%(day_name,st,date.time().hour,date.time().minute)
