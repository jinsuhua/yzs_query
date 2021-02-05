import json
import requests
from django.http import HttpRequest, HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serializers import *
from .models import *
from .config import *

import logging
logger = logging.getLogger("django")


class MyTokenObtainPairView(TokenObtainPairView):
    """
    自定义得到token username: 账号或者密码 password: 密码或者验证码
    """
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenViewBase):
    """
    自定义刷新token refresh: 刷新token的元素
    """
    serializer_class = TokenRefreshSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SSOReady(APIView):
    """
    跳转到登陆页面
    """
    permission_classes = []

    def get(self, request):
        uri = "{}?response_type=code&scope=read&client_id={}&redirect_uri={}&state=a5fd852f-c120-4ba1-89d0-d66dd3582bc9"\
            .format(sso_uri_code, client_id, redirect_uri_vue)
        logger.info("sso重定向到用户登陆页面{}，成功后返回code到redirect_uri".format(uri))
        #return Response("已跳转登陆页面，请等待用户登陆后返回的code")
        return HttpResponseRedirect(uri)


class SSOTokenView(APIView):
    """
    根据code去获取token
    """
    permission_classes = []

    def get(self, request):
        code = request.query_params.get('code')
        logger.info("sso_code:{}".format(code))

        username = "000"
        if code:
            post_data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri_vue,
                "grant_type": grant_type,
                "code": code
            }

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            res_token = requests.post(url=sso_uri_token, data=post_data, headers=headers)
            logger.info("根据code获取access_token----uri：{}, post 参数：{}".format(sso_uri_token, post_data))
            access_token = json.loads(res_token.text)['access_token']


            user_url = "{}?access_token={}&isAdUser=1".format(sso_uri_user, access_token)
            logger.info("根据token获取用户信息: {}".format(user_url))
            res_user = requests.get(user_url)
            user_json = json.loads(res_user.text)

            logger.info("用户信息：{}".format(user_json))
            pd = user_json["hcmData"]


            if pd:
                username = pd["uid"]
                logger.info("域账号：{}".format(username))


        rq = HttpRequest()
        rq.method = "POST"
        rq.META['CONTENT_TYPE'] = 'multipart/form-data'
        rq.META['user_defined'] = True
        #print(rq.POST)
        rq.POST['username'] = username
        return MyTokenObtainPairView.as_view()(rq)







