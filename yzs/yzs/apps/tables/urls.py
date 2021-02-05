from django.conf.urls import url
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

urlpatterns = [

    #url(r'^tables/(?P<tablename>\w{1,20})/$', views.TableSearchView.as_view()),
    url(r'^api/dbinfo/(?P<pk>\d+)/$', views.DBInfoViewSet.as_view({'delete': 'destroy'})),
]


router = SimpleRouter()  # 创建路由器(路由器只能结合视图集一起使用) 默认只为标准了增删改查行为生成路由信息,如果想让自定义的行为也生成路由需要在自定义行为上用action装饰进行装饰
router.register(r'api/businfo', views.BusInfoViewSet)  # 注册路由
router.register(r'api/dbinfo', views.DBInfoViewSet)  # 注册路由
router.register(r'api/tabinfo', views.TabInfoViewSet)  # 注册路由
router.register(r'api/tabmeta', views.TabMetaViewSet)  # 注册路由
router.register(r'api/tabmetahis', views.TabMetaHisViewSet)  # 注册路由
router.register(r'api/tabddl', views.TabDDLViewSet)  # 注册路由
router.register(r'api/tabddlhis', views.TabDDLHisViewSet)  # 注册路由
router.register(r'api/tabsamp', views.TabSampViewSet)  # 注册路由
#print(router.urls)
urlpatterns += router.urls  # 把生成好的路由拼接到urlpatterns

# SimpleRouter和DefaultRouter 只有一个区别,DefaultRouter会多生成一个根路由