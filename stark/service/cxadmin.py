from django.shortcuts import render,HttpResponse
class StarkConfig(object):
    def __init__(self,model,cxadmin_site):
        self.model = model
        self.cxadmin_site = cxadmin_site

    def changelist_view(self,request,*args,**kwargs):
        # if self
        return HttpResponse("列表")
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