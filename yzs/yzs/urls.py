"""yzs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework.settings import api_settings

#print(type(api_settings.DEFAULT_PERMISSION_CLASSES))

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^', include('users.urls')),
    url(r'^', include('tables.urls')),
    url(r'docs/', include_docs_urls(title='xxx')),
]
