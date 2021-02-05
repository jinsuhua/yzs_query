from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return self.username

    password = None
    first_name = None
    last_name = None
    is_superuser = None
    is_staff = None
    is_active = None
    email = None
    date_joined = None
    last_login = None

    #mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AccessLog(models.Model):

    uri = models.CharField(max_length=100, verbose_name='访问uri', help_text='访问uri')
    user_id = models.CharField(max_length=20, verbose_name='用户id', help_text='用户id')
    create_date = models.DateTimeField(auto_now_add=True, help_text='创建时间')

    class Meta:
        db_table = 'tb_access_log'
        verbose_name = '访问日志表'
        verbose_name_plural = verbose_name