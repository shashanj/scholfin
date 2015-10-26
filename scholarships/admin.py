from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
# Register your models here.

from .models import *

class loggedcountAdmin(admin.ModelAdmin):
    list_display =["scholarship","user_count",]

admin.site.register(scholarship,MyModelAdmin)
admin.site.register(field)
admin.site.register(caste)
admin.site.register(state)
admin.site.register(religion)
admin.site.register(level)
admin.site.register(abroad)
admin.site.register(interest)
admin.site.register(UserProfile)
# admin.site.register(loggedcount)
admin.site.register(loggedcount,loggedcountAdmin)
