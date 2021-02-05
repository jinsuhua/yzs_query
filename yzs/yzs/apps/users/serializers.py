from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, ** kwargs):
        super().__init__(*args, ** kwargs)
        del self.fields['password']

    '''
    token验证
    '''
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username #这个是你的自定义返回的
        #data['user_id'] = self.user.id #这个是你的自定义返回的

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        #fields = '__all__'
