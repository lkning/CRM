from django.shortcuts import render,HttpResponse
class StarkConfig(object):
    list_display=[]
    def __init__(self,model,cxadmin_site):
        self.model = model
        self.cxadmin_site = cxadmin_site

    def changelist_view(self,request,*args,**kwargs):
        """
                /stark/app01/userinfo/    self.model_class=models.UserInfo
        		/stark/app01/role/        self.model_class=models.Role
                :param request:
                :param args:
                :param kwargs:
                :return:
                """
        # 处理表头

        head_list = []
        for field_name in self.list_display:
            if isinstance(field_name, str):
                # 根据类和字段名称，获取字段对象的verbose_name
                verbose_name = self.model._meta.get_field(field_name).verbose_name
            else:
                verbose_name = field_name(self,is_header=True)
            head_list.append(verbose_name)

        # 处理表中的数据
        # [ UserInfoObj,UserInfoObj,UserInfoObj,UserInfoObj,]
        # [ UserInfo(id=1,name='alex',age=18),UserInfo(id=2,name='alex2',age=181),]
        data_list = self.model.objects.all()
        new_data_list = []
        for row in data_list:
            # row是 UserInfo(id=2,name='alex2',age=181)
            # row.id,row.name,row.age
            temp = []
            for field_name in self.list_display:
                if isinstance(field_name, str):
                    val = getattr(row, field_name)  # # 2 alex2
                else:
                    val = field_name(self, row)
                temp.append(val)
            new_data_list.append(temp)

        return render(request,'stark/changelist.html', {'data_list': new_data_list, 'head_list': head_list})



    def add_view(self,request,*args,**kwargs):
        return HttpResponse("添加页面")
    def history_view(self,request,*args,**kwargs):
        return HttpResponse("历史页面")
    def delete_view(self,request,*args,**kwargs):
        return HttpResponse("删除页面")
    def change_view(self,request,*args,**kwargs):
        return HttpResponse("修改页面")

    def get_urls(self):
        from django.conf.urls import url
        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$',self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/history/$',self.history_view, name='%s_%s_history' % info),
            url(r'^(.+)/delete/$',self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$',self.change_view, name='%s_%s_change' % info),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

class StarkSite(object):
    def __init__(self):
        self._registry = {}

    def register(self, model,starkconfig=None):
        if not starkconfig:
            starkconfig = StarkConfig
        self._registry[model] = starkconfig(model, self)

    def get_urls(self):
        from django.conf.urls import url, include
        urlpatterns=[]
        for model, model_admin in self._registry.items():
            urlpatterns += [
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(),'cxadmin',None
cxsite = StarkSite()