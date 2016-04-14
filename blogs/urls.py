# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""scholfin_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url, patterns
from django.conf import settings
from blogs.sitemaps import BlogSitemap
from blogs.rssfeed import *
from django.conf.urls.static import static
from django.contrib import admin

sitemaps = {
  'blogs' : BlogSitemap()
}

urlpatterns = [
    url(r'^$', 'blogs.views.index',name= 'home'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^sitemap\.xml$','django.contrib.sitemaps.views.sitemap',{'sitemaps':sitemaps}),
  	url(r'^rssfeed/$', LatestEntriesFeed()),
    url(
   		 r'^blog/view/(?P<slug>[^\.]+).html', 
   		 'blogs.views.view_post', 
  		  name='view_blog_post'),
	url(
   		 r'^blog/category/(?P<slug>[^\.]+).html', 
    	'blogs.views.view_category', 
    	name='view_blog_category'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
