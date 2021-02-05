from django.conf.urls import url
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenVerifyView

from . import views
from .views import *

urlpatterns = [
    # url(路径正则, 视图函数的名字)
     #url(r'^users/index/$', views.index),
     #url(r'^users/login/$', views.login_ready),
     #path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

     #url(r'^index/$', views.index, name='index'),
     # http://127.0.0.1:8000/users/sayhello
     # 路由匹配顺序是自上而下的, 定义子路由时一定要在最后多加一个$
     # 定义子路由时尽量在路由的最后加一个斜杠 会更加灵活
     #url(r'^say/$', views.say),

     #url(r'^sayhello/$', views.say_hello),


     path('sso/ready/', SSOReady.as_view(), name='sso_ready'),
     path('sso/token/', SSOTokenView.as_view(), name='sso_token'),

     # rest_framework_simplejwt自带的得到token
     path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     # 刷新JWT
     path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
     # 验证token
     path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

router = SimpleRouter()  # 创建路由器(路由器只能结合视图集一起使用) 默认只为标准了增删改查行为生成路由信息,如果想让自定义的行为也生成路由需要在自定义行为上用action装饰进行装饰
router.register(r'users', views.UserViewSet)  # 注册路由
#print(router.urls)
urlpatterns += router.urls  # 把生成好的路由拼接到urlpatterns
#print(urlpatterns)
