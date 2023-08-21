from apps.accounts.models import User
from apps.prm.models import Plan
from django.contrib.contenttypes.fields import ContentType
from django.db import models


# Create your models here.
class CommonCode(models.Model):

    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="common_code_creator",
    )

    content_type = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    content = models.JSONField(blank=True, default=list)

    class Meta:
        verbose_name_plural = "commoncodes"
