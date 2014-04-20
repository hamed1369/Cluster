# -*- coding:utf-8 -*-

__author__ = 'Hourshad'
from django.db import models
from django.contrib.auth.models import User


def __unicode__(self):
    if self.first_name and self.last_name:
        return u"%s %s" % (self.first_name, self.last_name)
    return self.username


setattr(User, '__unicode__', __unicode__)


class InternationalAccount(models.Model):
    GENDER = (
        (1, u"male"),
        (2, u"female")
    )
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    email = models.EmailField('e-mail address')
    gender = models.IntegerField(u"gender", choices=GENDER)
    country = models.CharField(u"country", max_length=50)
    residence_city = models.CharField(u"city", max_length=50)
    address = models.CharField(u"address", max_length=400, null=True, blank=True)
    telephone = models.CharField(u"telephone number", max_length=16, null=True, blank=True)
    mobile = models.CharField(u"mobile number", max_length=15, null=True, blank=True)
    project_summery = models.FileField(u"project summery", upload_to="project_summery",null=True, blank=True)
    created_on = models.DateField(u"registration date", auto_now_add=True)


class Account(models.Model):
    GENDER = (
        (1, u"مرد"),
        (2, u"زن")
    )
    gender = models.IntegerField(u"جنسیت", choices=GENDER, null=True, blank=True)
    # father_name     = models.CharField(u"نام پدر", max_length=30)
    national_code = models.BigIntegerField(u"کد ملی", null=True, blank=True)
    # identification_number = models.BigIntegerField(u"شماره شناسنامه")
    birth_date = models.DateField(u"تاریخ تولد", null=True, blank=True)
    residence_city = models.CharField(u"شهر محل اقامت", max_length=20, null=True, blank=True)
    telephone = models.CharField(u"تلفن ثابت", max_length=16, null=True, blank=True)
    mobile = models.CharField(u"تلفن همراه", max_length=15, null=True, blank=True)
    essential_telephone = models.CharField(u"تلفن ضروری", max_length=16, null=True, blank=True)
    address = models.CharField(u"آدرس", max_length=400, null=True, blank=True)
    created_on = models.DateField(u"تاریخ ایجاد", auto_now_add=True)

    class Meta:
        abstract = True


class Member(Account):
    EMPLOYMENT_STATUS = (
        (1, u"شاغل"),
        (2, u"دانشجو"),
    )
    MILITARY_STATUS = (
        (1, u"دارای کارت پایان خدمت"),
        (2, u"در حال خدمت"),
        (3, u"دارای کارت معافیت"),
    )
    EXEMPTION = (
        (1, u"معافیت تحصیلی"),
        (2, u"معافیت دائم")
    )
    cluster = models.ForeignKey('Cluster', verbose_name=u"خوشه", related_name="members", null=True, blank=True)
    user = models.OneToOneField(User, related_name="member")
    employment_status = models.IntegerField(u"وضعیت شغلی", choices=EMPLOYMENT_STATUS, null=True, blank=True)
    organization = models.CharField(u"محل کار", max_length=30, null=True, blank=True)
    military_status = models.IntegerField(u"وضعیت نظام وظیفه", choices=MILITARY_STATUS, null=True, blank=True)
    military_place = models.CharField(u"محل خدمت", max_length=30, null=True, blank=True)
    exemption_type = models.IntegerField(u"نوع معافیت", choices=EXEMPTION, null=True, blank=True)
    foundation_of_elites = models.BooleanField(u"عضویت در بنیاد ملی نخبگان", default=False)
    image = models.FileField(u"عکس", upload_to="member_images/", null=True, blank=True)
    # elite_certification = models.FileField(u"مدرک نخبگی", upload_to="elite_certificates/", null=True, blank=True)
    front_id_card = models.FileField(u"تصویر روی کارت ملی", upload_to="national_id_cards/", null=True, blank=True)
    # back_id_card        = models.FileField(u"تصویر پشت کارت ملی", upload_to="national_id_cards/", null=True, blank=True)
    education_certification = models.FileField(u"تصویر آخرین مدرک تحصیلی", upload_to="education_certificates",
                                               null=True, blank=True)
    arbiter_interest = models.BooleanField(u"تمایل به داوری دارم", default=False)

    domain = models.ForeignKey('Domain', verbose_name=u"حوزه فعالیت", related_name='members', null=True, blank=True,
                               on_delete=models.SET_NULL)

    is_confirmed = models.NullBooleanField(u"وضعیت", )

    class Meta:
        app_label = 'account'
        verbose_name = u"عضو خوشه"
        verbose_name_plural = u"اعضای خوشه"

    def __unicode__(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name) if (
            self.user.first_name and self.user.last_name) else u"%s" % self.user.username

    def delete(self, using=None):
        self.user.delete()
        super(Member, self).delete()


class Arbiter(Account):
    u"""
    داور
    """
    ARBITER_TITLES = (
        (1, u'پروفسور'),
        (2, u'دکتر'),
        (3, u'مهندس'),
    )
    title = models.IntegerField(u"عنوان", choices=ARBITER_TITLES, null=True, blank=True)
    user = models.OneToOneField(User, related_name="arbiter", null=True, blank=True)
    workplace = models.CharField(u"محل کار", max_length=30, null=True, blank=True)
    # field           = models.CharField(u"رشته", max_length=20)
    # professional    = models.CharField(u"گرایش تخصصی", max_length=20)
    # degree          = models.CharField(u"مرتبه علمی", max_length=20) # TODO : ابهام
    # office_phone    = models.CharField(u"تلفن مخل کار" , max_length=15)
    fax = models.CharField(u"فکس", max_length=15, null=True, blank=True)
    interested_domain = models.ManyToManyField('Domain', related_name="arbiters", verbose_name=u"حوزه های مورد علاقه")
    is_confirmed = models.NullBooleanField(u"تایید شده")

    invited = models.BooleanField(u"دعوت شده", default=False)
    invitation_key = models.CharField(u"کد دعوتنامه", max_length=200, null=True, blank=True)

    class Meta:
        app_label = 'account'
        verbose_name = u"داور"
        verbose_name_plural = u"داورها"

    def __unicode__(self):
        if self.user:
            if self.gender == 1:
                full_name = u"جناب آقای "
            else:
                full_name = u"سرکار خانم "
            full_name += self.get_title_display() or ''
            full_name += u" %s %s" % (self.user.first_name, self.user.last_name)
            return full_name
        else:
            return u"داور دعوت شده: %s" % self.invitation_key

    def delete(self, using=None):
        self.user.delete()
        super(Arbiter, self).delete()


class Supervisor(models.Model):
    user = models.OneToOneField(User, related_name="supervisor")
    mobile = models.CharField(u"تلفن همراه", max_length=15, null=True, blank=True)

    class Meta:
        app_label = 'account'
        verbose_name = u"ناظر"
        verbose_name_plural = u"ناظران"

    def __unicode__(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name) if (
            self.user.first_name and self.user.last_name) else u"%s" % self.user.username

    def delete(self, using=None):
        self.user.delete()
        super(Supervisor, self).delete()


#class UserDomain(models.Model):
#    user = models.OneToOneField(User, verbose_name=u"عضو", related_name='user_domain')
#    domain = models.ForeignKey('Domain', verbose_name=u"حوزه فعالیت", related_name='user_domain', null=True, blank=True, on_delete=models.SET_NULL)
#
#    class Meta:
#        app_label = 'account'
#        verbose_name = u"دامنه عضو"
#        verbose_name_plural = u"دامنه های عضو"
#
#    def __unicode__(self):
#        return u"%s - %s" % (self.user, self.domain or '---')


class Cluster(models.Model):
    name = models.CharField(u"نام خوشه", max_length=50)
    domains = models.ManyToManyField('Domain', related_name='clusters', verbose_name=u"حوزه فعالیت", ) # TODO : ابهام
    institute = models.CharField(u"دانشگاه / موسسه", max_length=30)
    head = models.OneToOneField(Member, verbose_name=u"سر خوشه", related_name='head_cluster')

    #user_domains= models.ManyToManyField(UserDomain, verbose_name=u"اعضا", related_name='clusters')

    CLUSTER_DEGREE = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
    )
    degree = models.IntegerField(u"درجه", choices=CLUSTER_DEGREE, default=3)

    created_on = models.DateField(u"تاریخ ایجاد", auto_now_add=True)

    class Meta:
        app_label = 'account'
        verbose_name = u"خوشه"
        verbose_name_plural = u"خوشه ها"

    def __unicode__(self):
        return self.name

    def get_members_and_links(self):
        res = []
        for member in self.members.order_by('-id'):
            user = member.user
            user_unicode = unicode(user)
            try:
                link = "/members/actions/?t=action&n=edit_member&i=%s" % member.id
            except:
                link = None
            res.append((user_unicode, link))
        return res

    def delete(self, using=None):
        self.members.all().delete()
        self.head.delete()
        super(Cluster, self).delete(using)


class Domain(models.Model):
    name = models.CharField(u"نام حوزه", max_length=40)
    confirmed = models.BooleanField(u"تایید شده", default=False)

    class Meta:
        verbose_name = u"حوزه"
        verbose_name_plural = u"حوزه ها"

    def __unicode__(self):
        if not self.confirmed:
            return unicode(self.name) + u"(تایید نشده)"
        else:
            return unicode(self.name)


def user_new_unicode(self):
    return u"%s %s" % (self.first_name, self.last_name) if (
        self.first_name and self.last_name) else u"%s" % self.username


User.__unicode__ = user_new_unicode