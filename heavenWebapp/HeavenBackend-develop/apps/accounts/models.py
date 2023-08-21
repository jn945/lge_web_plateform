from apps.groups.models import CustomGroup
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
    User,
)
from django.db import models

# Customgroup.


class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, email, username, name, password=None):
        if not email:
            raise ValueError("must have user email")
        if not username:
            raise ValueError("must have user username")
        if not name:
            raise ValueError("must have user name")
        user = self.model(
            email=self.normalize_email(email), username=username, name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, email, username, name, password=None):
        user = self.create_user(email, password=password, username=username, name=name)
        user.is_admin = True
        user.is_staff = True
        user.has_module_perms = True
        user.has_perm = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    email = models.EmailField(
        default="", max_length=100, null=False, blank=False, unique=True
    )
    username = models.CharField(
        default="", max_length=100, null=False, blank=False, unique=True
    )
    name = models.CharField(default="", max_length=100, null=False, blank=False)
    groups = models.ManyToManyField(
        CustomGroup, related_name="custom_groups_users111", blank=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 nickname으로 설정
    USERNAME_FIELD = "username"
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ["email", "name"]

    def __str__(self):
        return self.username

    # 권한 검사 list로
    def has_perms(self, perm, obj=None):
        # 잠시 해제 by 맹
        """
        if self.is_staff:
            return True
        perm_set = set([])
        for _group in self.groups.all():
            for inv_perm in _group.permissions.all():
                perm_set.add(inv_perm.codename)
        for req_perm in perm:
            if req_perm not in perm_set:
                return False
        """
        return True

    def has_perm(self, perm, obj=None):
        # 잠시 해제 by 맹
        """
        if self.is_staff:
            return True

        perm_set = set([])
        for _group in self.groups.all():
            for inv_perm in _group.permissions.all():
                perm_set.add(inv_perm.codename)
        for req_perm in perm:
            if req_perm not in perm_set:
                return False
        """
        return True

    def has_module_perms(self, app_label):
        return True


@property
def is_staff(self):
    return self.is_admin
