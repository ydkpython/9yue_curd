from yingun.service import v1
from app01 import models
from django.urls import reverse
from django.utils.safestring import mark_safe

class YinGunUser(v1.BaseYingun):
    def func(self, obj):
        name="{0}:{1}_{2}_change".format(self.site.namespace,self.app_label,self.model_name)
        url=reverse(name,args=(obj.pk,))
        return mark_safe("<a href='{0}'>编辑</a>".format(url))

    list_display=['id','user','email',func]



class YinGunRole(v1.BaseYingun):
    def func(self, obj):
        name="{0}:{1}_{2}_change".format(self.site.namespace,self.app_label,self.model_name)
        url=reverse(name,args=(obj.pk,))
        return mark_safe("<a href='{0}'>编辑</a>".format(url))

    list_display=['id','name',func]

v1.site.register(models.Userinfo,YinGunUser)
v1.site.register(models.Role,YinGunRole)