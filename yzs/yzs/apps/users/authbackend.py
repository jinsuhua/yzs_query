"""
实现自定义认证类
"""

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User

class MyLoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        #print("cccccccccccccccccccccccc")
        try:
            # 先按用户名查找
            user = User.objects.get(
                # username=="18588269037" or mobile=="18588269037"
                # Q(username=username) | Q(mobile=username) | Q(email=username)
                username=username
            )
            #print(user)
        except User.DoesNotExist as e:
            #print("11111111111111")
            return None

        #print("2222222222222")
        return user
        # 如果用户存在再校验密码
        # if user.check_password(password):
        #     print("22222222222222")
        #     return user
        # print("333333333333333")