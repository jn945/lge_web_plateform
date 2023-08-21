from apps.accounts.models import User
from django.db import models


class VirtualAnalysisRequest(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="writer_VA"
    )

    # 추후 foreign key with model 로 변경 예정
    model = models.CharField(max_length=100)
    cae_type = models.CharField(max_length=100)
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requester"
    )
    request_date = models.DateTimeField()
    start_date = models.DateTimeField()
    target_date = models.DateTimeField()
    complete_date = models.DateTimeField()
    cae_engineer = models.ForeignKey(
        User, blank=True, on_delete=models.CASCADE, related_name="cae_engineer"
    )
    cae_state = models.CharField(max_length=100, null=True)
    cae_result = models.CharField(max_length=100, null=True)
    report = models.CharField(max_length=100, null=True)

    event = models.CharField(max_length=100, null=True)
    cae_data = models.JSONField(blank=True, default=list)

    class Meta:
        verbose_name_plural = "virtualanalysisrequest"


class CAEData(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="cae_data_creator"
    )
    
    model = models.CharField(max_length=100)
    data_name = models.CharField(max_length=100)
    essential_info = models.BooleanField(null=True)
    exist = models.BooleanField(null=True)
    data_form = models.CharField(max_length=100)
    data = models.CharField(null=True, max_length=400)

    class Meta:
        verbose_name_plural = "caedata"
