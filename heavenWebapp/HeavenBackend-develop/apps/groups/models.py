from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.db import models


class CustomGroup(Group):
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(
        default="", max_length=100, null=False, blank=False, unique=True
    )
    description = models.TextField(max_length=1000, default=None)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "customgroups"
        verbose_name = "customgroup"
