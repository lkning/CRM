
class StarkConfig(object):
    def __init__(self,model,cxadmin_site):
        self.model = model
        self.cxadmin_site = cxadmin_site
    def changelist_view(self):
        pass
    def add_view(self):
        pass
    def history_view(self):
        pass
    def delete_view(self):
        pass
    def change_view(self):
        pass

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