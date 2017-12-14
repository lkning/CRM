from stark.service import cxadmin
from app01 import models
from django.utils.safestring import mark_safe
# class UserConfig(cxadmin.StarkConfig):
#     pass
# cxadmin.cxsite.site.register(models.UserType,UserConfig)

class UserInfoConfig(cxadmin.StarkConfig):

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" name="pk" value="%s" />' %(obj.id,))
    def edit(self,obj=None,is_header=False):
        if is_header:
            return '编辑'
        return mark_safe('<a href="/edit/%s">编辑</a>' %(obj.id,))

    list_display = [checkbox,'id','name',edit]

cxadmin.cxsite.register(models.UserInfo,UserInfoConfig) # UserInfoConfig(UserInfo,)


class RoleConfig(cxadmin.StarkConfig):
    list_display = ['name',]
cxadmin.cxsite.register(models.Role,RoleConfig) # StarkConfig(Role)

class UserTypeConfig(cxadmin.StarkConfig):
    list_display = ['id','xxx']
cxadmin.cxsite.register(models.UserType,UserTypeConfig) # StarkConfig(Role)

