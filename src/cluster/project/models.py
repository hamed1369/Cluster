# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models, transaction
from cluster.account.account.models import Member, Cluster, Domain, Arbiter, Supervisor
from cluster.utils.calverter import gregorian_to_jalali
from cluster.utils.messages import MessageServices, SMSService
from cluster.utils.permissions import PermissionController


class Project(models.Model):
    CONFIRM_TYPE = (
        (1, u"ندارد"),
        (2, u"تاییدیه سازمان پژوهش های علمی و صنعتی ایران"),
        (3, u"برگزیده جشنواره خوارزمی"),
        (4, u"برگزیده جشنواره رازی"),
        (5, u"برگزیده جشنواره شیخ بهائی"),
        (6, u"برگزیده جشنواره فارابی"),
        (7, u"سایر دانشگاه ها و مراکز دولتی"),
    )
    STATE = (
        (1, u"ایده"),
        (2, u"مدل و ماکت و تکمیل پژوهش"),
        (3, u"نمونه آزمایشی"),
        (4, u"در حال تولید"),
    )
    REJECT_STATE = -1
    MIDDLE_CONFIRM_STATE = 1
    CONFIRM_STATE = 3
    STATUS = (
        (-1, u"رد شده"),
        (0, u"در مرحله درخواست"),
        (1, u"تایید مرحله اول"),
        #(2, u"تاییدشده توسط داور"),
        (3, u"تایید مرحله دوم"),
        (4, u"تکمیل شده"),

    )
    title = models.CharField(u"عنوان طرح", max_length=300)
    confirmation_type = models.IntegerField(u"تاییدیه علمی و نوآوری", choices=CONFIRM_TYPE, default=1)
    certificate_image = models.FileField(u"تصویر مدرک تاییدیه", upload_to="project_certificate_images/", null=True,
                                         blank=True)
    has_patent = models.BooleanField(u"دارای ثبت اختراع", default=False)
    patent_number = models.CharField(u"شماره ثبت اختراع", max_length=20, null=True, blank=True)
    patent_date = models.DateField(u"تاریخ ثبت اختراع", null=True, blank=True)
    patent_certificate = models.FileField(u"مدرک ثبت اختراع", upload_to="project_patents/", null=True, blank=True)
    patent_request = models.BooleanField(u"تقاضای ثبت اختراع", default=False)
    domain = models.ForeignKey(Domain, verbose_name=u"حوزه علمی و کاربردی طرح", related_name='projects',
                               on_delete=models.SET_NULL, null=True)
    summary = models.CharField(u"خلاصه طرح", max_length=2000)
    keywords = models.CharField(u"کلید واژه", max_length=100)
    innovations = models.CharField(u"نوآوری های طرح", max_length=300)
    state = models.IntegerField(u"مرحله", choices=STATE)
    attended_members = models.ManyToManyField(Member, verbose_name=u"اعضای مربوط به طرح",
                                              related_name='projects_attended')
    project_status = models.IntegerField(u"مرحله داوری", choices=STATUS, default=0)

    single_member = models.ForeignKey(Member, verbose_name=u"عضو", null=True, blank=True)
    cluster = models.ForeignKey(Cluster, verbose_name=u"خوشه", null=True, blank=True)

    supervisor = models.ForeignKey(Supervisor, verbose_name=u"ناظر طرح", null=True, blank=True,
                                   on_delete=models.SET_NULL)
    score = models.FloatField(verbose_name=u"امتیاز", null=True, blank=True)

    class Meta:
        verbose_name = u"طرح"
        verbose_name_plural = u"طرح ها"

    def __unicode__(self):
        return self.title


class ProjectMilestone(models.Model):
    created_on = models.DateField(verbose_name=u"تاریخ ایجاد", auto_now_add=True)
    comment = models.CharField(verbose_name=u"توضیح", max_length=200)
    project = models.ForeignKey(Project, verbose_name=u"طرح", related_name='milestones')
    milestone_date = models.DateField(verbose_name=u"زمان موعد")
    is_announced = models.BooleanField(u"ابلاغ شده", default=False)

    class Meta:
        verbose_name = u"مرحله موعد"
        verbose_name_plural = u"مراحل موعد"

    @classmethod
    @transaction.commit_on_success
    def check_milestones(cls):
        import datetime
        from cluster.message.models import Message

        two_days_later = datetime.date.today() + datetime.timedelta(days=2)
        milestones = ProjectMilestone.objects.filter(milestone_date__lte=two_days_later, is_announced=False)
        body = u"""
        موعد های طرح های زیر گذشته اند یا نزدیک هستند:
        """
        i = 1
        if not milestones:
            return

        admin_users = PermissionController.get_admins()

        for milestone in milestones:
            receiver = milestone.project.single_member.user if milestone.project.single_member else milestone.project.cluster.head.user
            receiver_mobile = milestone.project.single_member.mobile if milestone.project.single_member else milestone.project.cluster.head.mobile
            section = u"""
                 موعد  %s  مربوط به طرح %s  برای زمان  %s
            """ % (milestone.comment, milestone.project.title, gregorian_to_jalali(milestone.milestone_date))
            Message.send_message(admin_users[0], title=u"موعدهای گذشته یا نزدیک", body=body, receivers=[receiver])
            message = MessageServices.get_title_body_message(title=u"موعد طرح زیر گذشته یا نزدیک است:",
                                                             body=section)
            MessageServices.send_message(subject=u"موعد طرح", message=message, user=receiver)
            SMSService.send_sms(message=u"موعد طرح زیر گذشته یا نزدیک است:" + '\n' + section,
                                to_numbers=[receiver_mobile])
            body += '\n' + unicode(i) + u'- ' + section.strip()
            i += 1
            milestone.is_announced = True
            milestone.save()
            if milestone.project.supervisor:
                MessageServices.send_message(subject=u"موعد طرح", message=message,
                                             user=milestone.project.supervisor.user)

        #message = MessageServices.get_title_body_message(title=u"موعد های طرح های زیر گذشته اند یا نزدیک هستند:",
        #                                                 body=body)
        Message.send_message(admin_users[0], title=u"موعدهای گذشته یا نزدیک",
                             body=body,
                             receivers=admin_users)

        #for user in admin_users:
        #    MessageServices.send_message(subject=u"موعدهای طرح", message=message, user=user)


class ProjectComment(models.Model):
    created_on = models.DateField(verbose_name=u"تاریخ ایجاد", auto_now_add=True)
    comment = models.TextField(verbose_name=u"توضیح", max_length=1000)
    project = models.ForeignKey(Project, verbose_name=u"طرح", related_name='comments')
    user = models.ForeignKey(User, verbose_name=u"کاربر مربوطه")
    seen_by_member = models.BooleanField(verbose_name=u"مشاهده توسط متقاضی", default=False)

    class Meta:
        verbose_name = u"توضیح طرح"
        verbose_name_plural = u"توضیح های طرح"

    def __unicode__(self):
        return self.comment


class ProjectArbiter(models.Model):
    created_on = models.DateField(verbose_name=u"تاریخ ایجاد", auto_now_add=True)
    project = models.ForeignKey(Project, verbose_name=u"طرح مربوطه", related_name='project_arbiters')
    arbiter = models.ForeignKey(Arbiter, verbose_name=u"داور مربوطه", related_name='project_arbiters')
    comment = models.TextField(verbose_name=u"نظر کلی", max_length=1000, null=True, blank=True)
    attachment = models.FileField(u"بارگزاری فرم داوری", upload_to="project_arbiter_attachments/", null=True,
                                  blank=True)
    confirmed = models.BooleanField(verbose_name=u"تاییدنهایی شده", default=False)
    confirm_date = models.DateField(verbose_name=u"تاریخ تاییدنهایی", null=True, blank=True)

    class Meta:
        verbose_name = u"داوری طرح"
        verbose_name_plural = u"داوری های طرح"

    def __unicode__(self):
        un = u"طرح %s - داور %s" % (self.project, self.arbiter)
        if not self.confirmed:
            return unicode(un) + u"(تایید نهایی نشده)"
        else:
            return unicode(un)

    def save(self, force_insert=False, force_update=False, using=None):
        import datetime

        if self.confirmed is True:
            self.confirm_date = datetime.date.today()
        instance = super(ProjectArbiter, self).save(force_insert, force_update, using)
        return instance
