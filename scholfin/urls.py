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
from scholarships import views
from scholarships import sorting
from scholarships import gov_pri_comp
from scholarships.sitemaps import ScholarshipSitemap
from scholarships.rssfeed import *

sitemaps = {
    'scholarships' : ScholarshipSitemap()
}

urlpatterns = [
    url(r'^$', views.index , name='index' ),
    url(r'^login/' , views.login_page , name='login'),
    url(r'^forgotpassword/' , views.forgot_password , name='forgotpassword'),
    url(r'^signup/' , views.signup , name='signup'),
    url(r'^fbsignup/' , views.fbsignup , name='fbsignup'),
    url(r'^googlesignup_process/' , views.googlesignup_process , name='googlesignup_process'),
    url(r'^fbsignup_process/' , views.fbsignup_process , name='fbsignup_process'),
    url(r'^signup-complete/' , views.signup_complete , name='signup_complete'),
    url(r'^a78shfbwifhbiwh324b2r2kjvr3h4brl3hb4r13hbrl/', include(admin.site.urls)),
    url(r'^signupprocess/' , views.signupprocess , name='signup'),
    url(r'^dashboard/',views.dashboard , name='dashboard'),
    url(r'^logout/',views.logout_user , name='logout'),
    url(r'^scholarships/government/' ,gov_pri_comp.gov , name='government'),
    url(r'^scholarships/private/' ,gov_pri_comp.pri , name='private'),
    url(r'^scholarships/abroad/' ,sorting.abroad_only , name='abroad'),
    url(r'^scholarships/india/' ,sorting.india_only , name='india'),
    url(r'^scholarships/competitions/' ,gov_pri_comp.comp , name='competition'),
    url(r'^scholarship-details/(?P<scholarship_name>[a-z,A-Z,0-9-]+)/$', views.detail,name='detail'),
    url(r'^scholarships/state/(?P<scholarship_state>[a-z,A-Z -]+)/$', sorting.state_only, name='states'),
    url(r'^scholarships/interests/$', sorting.interest_only, name='interests'),
    url(r'^scholarships/caste/$', sorting.caste_only , name='caste'),
    url(r'^scholarships/religion/$', sorting.religion_only , name='religion'),
    url(r'^profile/$', views.profilepage , name='profile'),
    url(r'^profilechange/$', views.profilechange , name='profilechange'),
    url(r'^sitemap\.xml$','django.contrib.sitemaps.views.sitemap',{'sitemaps':sitemaps}),
    url(r'^rssfeed/$', LatestEntriesFeed()),
    url(r'^atom/$', AtomSiteNewsFeed()),
    url(r'^contact_us/$', views.contact_us , name='contact_us'),
    url(r'^about_us/$',views.about_us),
    url(r'^internship/$',views.internship,name='internship'),
]
