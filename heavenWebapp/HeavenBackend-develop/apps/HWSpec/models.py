from apps.accounts.models import User
from apps.CommonCode.models import CommonCode
from apps.HWCheck.models import HWCheck, HWCheckRow
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Soc(models.Model):
    # 1. id, 생성자, 생성 시간
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    user_compare = models.ManyToManyField(
        User, blank=True, related_name="soc_user_compare"
    )

    # 2. 필터
    name = models.CharField(max_length=100, unique=True)
    year = models.CharField(max_length=100)
    resolution = models.CharField(max_length=100)

    # 3. JSON Field
    fields = models.JSONField(blank=True, default=list)

    class Meta:
        verbose_name_plural = "soces"

    # # soc 생성 시, name으로 nmdis 자동생성
    # def save(self, *args, **kwargs):
    #     created = not self.pk
    #     super().save(*args, **kwargs)
    #     if created:
    #         ins = HWCheck.objects.create(soc=self.name, device="SoC")
    #         common_code = CommonCode.objects.get(
    #             name="hw_check_row", content_type="hwcheck_hwcheckrow"
    #         )
    #     if common_code.exists():
    #         hw_check_ins = HWCheck.objects.create(soc=self.name)
    #         for row in common_code.content:
    #             # row.pop("common_user")
    #             row["hw_check_id"] = hw_check_ins
    #             HWCheckRow.objects.create(**row)


class SocInfo(models.Model):
    # 1. id, 생성자, 생성 시간
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    row_name_1 = models.CharField(max_length=100)
    row_name_2 = models.CharField(max_length=100, null=True)
    value_list = models.JSONField(default=list)

    class Meta:
        verbose_name_plural = "soc_categorys"


class Power(models.Model):
    # 1. id, 생성자, 생성 시간
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    user_compare = models.ManyToManyField(
        User, blank=True, related_name="power_user_compare"
    )
    # 2. 필터
    name = models.CharField(max_length=100, unique=True)
    year = models.CharField(max_length=100, null=True)
    device = models.CharField(max_length=100, null=True)

    # 3. JSON Field
    fields = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "powers"


class PowerInfo(models.Model):
    # 1. id, 생성자, 생성 시간
    id = models.AutoField(primary_key=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    row_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, null=True)
    unit = models.CharField(max_length=100, null=True)
    category = models.TextField(default=list)
    select_list = models.JSONField(default=list)

    class Meta:
        verbose_name_plural = "power_categorys"


@receiver(pre_save, sender=Soc)
def update_Document_from_HWCheck(sender, instance, **kwargs):
    if instance.pk is None:

        # HW Check 생성 시, 준용 document 복사해오는 동작
        name = instance.name
        common_code = CommonCode.objects.filter(
            name="hw_check_row", content_type="hwcheck_hwcheckrow"
        )
        if common_code.exists():
            print("do it")
            hw_check_ins = HWCheck.objects.create(soc=name)
            for row in common_code[0].content:
                row.pop("common_user")
                row["hw_check_id"] = hw_check_ins
                # print(**row)
                HWCheckRow.objects.create(**row)
        else:
            HWCheck.objects.create(soc=name)
