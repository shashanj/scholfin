from django.conf.urls import include, url
from django.contrib import admin
import views


urlpatterns = [
    url(r'^get_institutes/', views.getInstitutes , name='getInstitutes' ),
    url(r'^get_scholarships/', views.getScholarships , name='getScholarships' ),
]