from apps.accounts.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save

# from django.dispatch import receiver
# from heaven.common.email import send_email

# from heaven.common.models import CustomeModel


class PlanInfo(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    year = models.CharField(max_length=100)
    device_and_tool = models.JSONField()
    inch_size = models.JSONField()

    class Meta:
        verbose_name_plural = "plans"


class Plan(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    year = models.CharField(max_length=100)
    plan_name = models.CharField(max_length=100, unique=True)
    device_and_tool = models.JSONField()
    inch_size = models.JSONField()

    class Meta:
        verbose_name_plural = "plans"


class PlanGroupInfo(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    plan_type = models.CharField(max_length=100, null=True)
    details = models.JSONField(blank=True)

    class Meta:
        verbose_name_plural = "plangroupinfos"


class PlanGroup(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=100, null=True)
    group_name = models.CharField(max_length=100, null=True, unique=True)
    description = models.CharField(max_length=400, null=True)
    details = models.JSONField(blank=True)

    class Meta:
        verbose_name_plural = "plangroups"


class PlanSeries(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    device = models.CharField(max_length=100)
    tool = models.CharField(max_length=100)
    inch_size = models.CharField(max_length=100)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    plan_group = models.JSONField(blank=True)


# @receiver(post_save, sender=Plan)
# def send_email_on_model_change(sender, instance, created, **kwargs):
#     if created:
#         # 새로운 인스턴스가 생성되었을 때
#         email_title = "New PlanSeries Created"
#         email_content = f"New PlanSeries with ID {instance.id} has been created."
#         recipients = ["mksong@intellicode.co.kr"]  # 이메일 수신자 지정
#     else:
#         # 인스턴스가 업데이트되었을 때
#         email_title = "PlanSeries Updated"
#         email_content = f"PlanSeries with ID {instance.id} has been updated."
#         recipients = ["mksong@intellicode.co.kr"]  # 이메일 수신자 지정

#     send_email(email_title, email_content, recipients)


# post_save.connect(send_email_on_model_change, sender=Plan)
# post_delete.connect(send_email_on_model_delete, sender=Plan)
