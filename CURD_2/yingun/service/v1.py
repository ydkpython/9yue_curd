from django.shortcuts import HttpResponse,render,redirect
from django.conf.urls import url,include
from django.urls import reverse
from django.db.models.query_utils import DeferredAttribute

class BaseYingun:
    list_display = '__all__'
    def __init__(self,model_class,site):
        self.model_class=model_class #模块类名
        self.site=site    #site是YinGun实例化的类
        self.app_label=self.model_class._meta.app_label
        self.model_name=self.model_class._meta.model_name
        self.info=self.app_label,self.model_name
        self.change_display='__all__'

    @property
    def urls(self):
        urlpatterns=[
            url(r'^$',self.list_view,name='%s_%s_list'%self.info),
            url(r'^add/$',self.add_view,name='%s_%s_add'%self.info),
            url(r'^(.+)/delete/$',self.del_view,name='%s_%s_delete'%self.info),
            url(r'^(.+)/change/$',self.change_view,name='%s_%s_change'%self.info),
        ]
        #进行路由分发时,返回值必须是元组,但是当是include进行导入模块进行分发时,返回值的变量是urlpatterns时,
        #只要保证urlpatterns是一个列表就行了,因为include会自动给urlpatterns 添加app_name,namespace组成元组
        #include 与urlpatterns必须成对出现
        return urlpatterns

    def list_view(self,request):
        result_list=self.model_class.objects.all()
        url_lis = reverse('yingun:%s_%s_list' % self.info)
        context = {
            'result_list':result_list,
            'list_display':self.list_display,
            'ygadmin_obj':self,
            'url':url_lis
        }


        return render(request, 'yg/yg_list.html', context)

    def add_view(self,request):
        url_lis = reverse('yingun:%s_%s_list' % self.info)
        print(url_lis)
        return HttpResponse('add')


    def del_view(self,request,pk):
        return HttpResponse('del')

    def change_view(self,request,pk):
        if request.method == 'GET':
            obj=self.model_class.objects.filter(pk=pk).first()
            context={
                'obj':obj,
                'list_display':self.list_display,
                'ygadmin_obj': self,
            }
            # return HttpResponse('change')
            return render(request,'yg/yg_change.html',context)
        else:
            change_dic={}
            for row in self.list_display:
                if request.POST.get(row):
                    change_dic[row]=request.POST.get(row)
            self.model_class.objects.filter(pk=pk).update(**change_dic)

            url=reverse("yingun:%s_%s_list"%self.info)
            return redirect(url)



class Yingun:
    def __init__(self):
        self._registry={}
        self.namespace='yingun'
        self.app_name='yingun'

    def register(self,model_class,xx=BaseYingun):
        self._registry[model_class]=xx(model_class,self)

    def get_urls(self):

        ret = [
            url(r'^login/',self.login,name='login'),
            url(r'^logout/',self.logout,name='logout'),

        ]
        for model_cls,yg_obj in self._registry.items():
            #yd_boj是BaseYingun实例化的对象
            app_label=model_cls._meta.app_label
            model_name=model_cls._meta.model_name

            ret.append(url(r'^%s/%s/'%(app_label,model_name),include(yg_obj.urls))) #通过include进行的

        return ret

    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.namespace

    def login(self,request):
        return HttpResponse('login')

    def logout(self,request):
        return HttpResponse('logout')

site=Yingun()
