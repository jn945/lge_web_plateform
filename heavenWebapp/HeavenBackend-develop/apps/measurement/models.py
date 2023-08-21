from datetime import datetime, timedelta

import reversion
from apps.accounts.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class TestItemInfo(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    test_item = models.CharField(max_length=100, null=True)
    sub_test_item = models.CharField(max_length=100, default=5)
    default_period = models.IntegerField(default=5, null=True)
    working_day_standard = models.BooleanField(default=False)
    period_overlap_possible = models.BooleanField(default=False)
    engineer_list = models.JSONField(default=list)
    default_result_format = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "testiteminfos"
        # managed = False


@reversion.register
class MeasurementRequest(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    model = models.CharField(max_length=100, null=True)
    test_item = models.CharField(max_length=100, null=True)
    sub_test_item = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)

    requester = models.CharField(max_length=100, null=True)
    engineer = models.CharField(max_length=100, null=True)  # User 와 m2m field로 전환예정
    target_date = models.DateTimeField(null=True)

    # request 일자
    request_date = models.DateTimeField(auto_now_add=True, null=True)
    # request 시, 요청 일자
    scheduled_date = models.JSONField(default=dict, blank=True)
    # default={"start": datetime.now(), "end": datetime.now() + timedelta(days=5)})

    # 실제 measurement 일자
    excuted_date = models.JSONField(default=dict, blank=True)

    # 예약 일자
    job_id = models.JSONField(max_length=100, default=dict, blank=True)

    reject_commet = models.TextField(null=True)
    comfirm_comment = models.TextField(null=True)
    comment = models.TextField(null=True)
    result = models.CharField(max_length=100, null=True)
    grade = models.CharField(max_length=100, null=True)
    event = models.CharField(max_length=100, null=True)
    tool_options = models.JSONField(blank=True, default=list)

    class Meta:
        verbose_name_plural = "measurementrequests"
        # managed = False


@reversion.register()
class Result(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="creator"
    )

    request = models.ForeignKey(
        MeasurementRequest, on_delete=models.CASCADE, null=True, related_name="requset"
    )
    test_item = models.CharField(max_length=100, null=True)
    sub_test_item = models.CharField(max_length=100, null=True)
    result = models.CharField(max_length=100, null=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    engineer = models.ManyToManyField(User, blank=True, related_name="engineer")

    # request 일자
    request_date = models.DateTimeField(auto_now_add=True, null=True)
    target_date = models.DateTimeField(null=True)
    # 실제 measurement 일자
    scheduled_date = models.JSONField(default=dict)
    excuted_date = models.JSONField(default=dict)
    jira_page = models.CharField(max_length=100, null=True)

    request = models.ForeignKey(
        MeasurementRequest, on_delete=models.CASCADE, null=True, related_name="requset"
    )
    graphics = models.JSONField(default=list)
    data = models.TextField(null=True)

    class Meta:
        verbose_name_plural = "measurementrequsets"
        # managed = False


# class Result(models.Model):
#     id = models.AutoField(primary_key=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     creator = models.ForeignKey(
#         User, on_delete=models.CASCADE, null=True, related_name="creator"
#     )

#     # serveer_name =
#     # server_ip =
#     # server_port =
#     # group_name =
#     # team_name =
#     # location =
#     # image_judgement_option =
#     # cmd_judgement_option =

#     class Meta:
#         verbose_name_plural = "measurementrequsets"
#         # managed = False
