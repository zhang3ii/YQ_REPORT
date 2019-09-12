"""untitled3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/page/', cache_page(0)(views.WordSearch), name='页面'),
    url(r'^api/update/', views.collect_api, name='更新'),
    url(r'^api/report/', views.today_report, name='日期周报'),
    url(r'^api/report_list/', views.group_time, name='周报列表'),
    url(r'^api/delete_report/', views.delete_report, name='删除周报'),
    url(r'^api/edit/', views.update_report, name='编辑周报'),
    url(r'^api/delete/', views.delete_report_by_id, name='周报删除'),
    url(r'^api/add/', views.add_data, name='添加数据'),
]
