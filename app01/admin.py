from django.contrib import admin
from app01 import models
# Register your models here.
class UserConfig(admin.ModelAdmin):
    pass
admin.site.register(models.UserType)
