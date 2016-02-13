"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from provider import views


urlpatterns = [
    url(r'^$', views.index , name='index' ),
    url(r'^login/$', views.login_user , name='login' ),
    url(r'^logout/$', views.logout_user , name='logout'),
    url(r'^signup/$', views.signup , name='signup' ),
    url(r'^getactivity/$', views.getactivity , name='activity' ),
    url(r'^dashboard/$', views.dashboard , name='dashboard'),
    url(r'^stats/(?P<scholarship_name>[a-z,A-Z,0-9-]+)$', views.details , name='dashmboard'),
    url(r'^response/(?P<scholarship_name>[a-z,A-Z,0-9-]+)$', views.response , name='response'),
    url(r'^shortlist/(?P<scholarship_name>[a-z,A-Z,0-9-]+)$', views.shortlist , name='shortlist'),
    url(r'^select/(?P<scholarship_name>[a-z,A-Z,0-9-]+)$', views.select , name='select'),
    url(r'^reject/(?P<scholarship_name>[a-z,A-Z,0-9-]+)$', views.reject , name='reject'),
    url(r'^action/$', views.action , name='action'),
    url(r'^task/$', views.task , name='task'),
    url(r'^selected/$', views.selected , name='selected'),
    url(r'^undo-reject/$', views.unreject , name='unreject'),
    url(r'^change-password/$', views.change_password , name='changepassword'),
    url(r'^download/$', views.genfiles , name='genfiles'),
    url(r'^form-download/$', views.form , name='form'),
    url(r'^multi_action/$', views.multi_action , name='multi_action'),
]