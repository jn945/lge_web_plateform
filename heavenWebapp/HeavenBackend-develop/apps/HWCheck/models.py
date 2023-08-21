import reversion
from apps.accounts.models import User
from django.db import models, transaction
from django.db.models.signals import post_save, pre_save

# from django.dispatch import receiver

# from heaven.common.email import apply_emailing


class HWCheckInfo(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="hw_check_info_creator"
    )
    main_part = models.CharField(max_length=100)
    sub_part = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    required_sw_function = models.CharField(max_length=100, null=True)
    hw_action = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = "hwcheckinfos"

    @classmethod
    def get_class_name(cls):
        return cls.__name__


class HWCheck(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="hw_check_creator"
    )
    device = models.CharField(max_length=100, null=True)
    tool = models.CharField(max_length=100, null=True)
    soc = models.CharField(max_length=100)
    main_model_name = models.CharField(max_length=100, null=True)
    sub_model_name = models.JSONField(default=list)
    note = models.CharField(max_length=100, null=True)
    is_done = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = "hwchecks"

    @classmethod
    def get_class_name(cls):
        return cls.__name__


class HWCheckRow(models.Model):

    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="hw_check_row_creator"
    )

    hw_check_id = models.ForeignKey(HWCheck, on_delete=models.CASCADE, null=True)
    main_part = models.CharField(max_length=100, null=True, blank=True)
    sub_part = models.CharField(max_length=100, null=True, blank=True)
    item = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    required_sw_function = models.CharField(max_length=100, null=True, blank=True)
    hw_action = models.CharField(max_length=100, null=True)
    common_user = models.ManyToManyField(
        User,
        blank=True,
        related_name="hw_check_row_exector",
    )
    due_date = models.CharField(max_length=100, null=True, blank=True)
    progress = models.CharField(max_length=100, default="Not started", blank=True)
    document_id = models.IntegerField(null=True, blank=True)
    result = models.CharField(max_length=100, null=True, blank=True)
    history_comment = models.TextField(null=True, blank=True)
    linked_db = models.CharField(max_length=100, null=True, blank=True)
    copy_from = models.CharField(max_length=100, null=True, blank=True)
    copy_from_document_id = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "hwcheckrows"

    @classmethod
    def get_class_name(cls):
        return cls.__name__


@reversion.register
class Document(models.Model):

    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="document_creator"
    )

    # copy_from = models.CharField(max_length=100, default="", null=True)
    # copy_from_document_id = models.IntegerField(null=True)
    # common_user = models.ManyToManyField(
    #     User, blank=True, related_name="document_exector", default=list
    # )
    # due_date = models.CharField(max_length=100, null=True)
    # progress = models.CharField(max_length=100, null=True)
    result = models.CharField(max_length=100, null=True)
    linked_db = models.CharField(max_length=100, null=True)
    comment = models.TextField(null=True)

    hw_check_row = models.ForeignKey(HWCheckRow, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "hwcheck_documnets"

    @classmethod
    def get_class_name(cls):
        return cls.__name__


# apply_emailing()
