from apps.groups.models import CustomGroup
from apps.measurement.models import MeasurementRequest, TestItemInfo
from apps.prm.models import Plan
from django.contrib import admin

from .models import User

# Register your models here.
admin.site.register(User)
admin.site.register(CustomGroup)
admin.site.register(Plan)
admin.site.register(TestItemInfo)
admin.site.register(MeasurementRequest)
