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
from django.contrib import admin
from custom_admin import views


urlpatterns = [
    url(r'^$', views.index , name='index' ),
    url(r'^all/' , views.all_scholarship , name='all_scholarship'),
    url(r'^dc/' , views.deadline_crossed , name='deadline_crossed'),
    url(r'^do/' , views.deadline_open , name='deadline_open'),
    url(r'^dlc/' , views.deadline_launch_and_closed , name='deadline_launch_and_closed'),
    url(r'^dt1/' , views.deadline_type_1 , name='deadline_type_1'),
    url(r'^dt2/' , views.deadline_type_2 , name='deadline_type_2'),
    url(r'^dt3/' , views.deadline_type_3 , name='deadline_type_3'),
    url(r'^a0/' , views.amount_equal_0 , name='amount_equal_0'),
    url(r'^weekly_update/' , views.weekly_update , name='weekly_update'),
    url(r'^send_weekly_update/' , views.send_weekly_update , name='send_weekly_update'),
    url(r'^scholarship_diff/' , views.scholarship_diff , name='scholarship_diff'),
    url(r'^cal_scholarship_diff/' , views.cal_scholarship_diff , name='cal_scholarship_diff'),
    url(r'^update_scholarship_source/' , views.update_scholarship_source , name='update_scholarship_source'),
    url(r'^scholarships/add/' , views.add_scholarship , name='add_scholarship'),
    url(r'^scholarships/view/' , views.view_scholarships , name='view_scholarships'),
    url(r'^scholarships/edit/(?P<scholarship_id>[0-9]+)' , views.edit_scholarship , name='edit_scholarship'),

]