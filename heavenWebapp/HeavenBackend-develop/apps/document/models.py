import reversion
from apps.accounts.models import User
from django.db import models


# Create your models here.
@reversion.register
class ProductSpecification(models.Model):

    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="product_specification_creator",
    )

    year = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)
    revision = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    editor_type = models.CharField(max_length=100, null=True)
    revision_date = models.CharField(max_length=100, null=True)
    created_date = models.DateField(auto_now_add=True)
    connection_db = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="product_specification_owner",
    )
    data = models.TextField(null=True)
    db = models.JSONField(blank=True, default=dict)

    class Meta:
        verbose_name_plural = "productspecifications"
        db_table = "document_productspecification"
