from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
# Register your models here.

from .models import *

class loggedcountAdmin(admin.ModelAdmin):
    list_display = ["scholarship","user_count",]

class UserProfileAdmin(admin.ModelAdmin):
	search_fields = ['user__email','user_income',]
	list_display = ['user','user_level','user_field','get_date_joined','get_last_login']
	list_filter = ['user_field__field_name','user_level__level_name','user_caste__caste_name','user_religion__religion_name','user_abroad__abroad_name','user_gender','user_income','user_disability','user_state__state_name']
	
	def get_last_login(self,obj):
		return obj.user.last_login
	get_last_login.admin_order_field  = 'user__last_login'  #Allows column order sorting
	get_last_login.short_description = 'last_login'


	def get_date_joined(self,obj):
		return obj.user.date_joined
	get_date_joined.admin_order_field  = 'user__date_joined'  #Allows column order sorting
	get_date_joined.short_description = 'Date joined'

admin.site.register(scholarship,MyModelAdmin)
admin.site.register(field)
admin.site.register(caste)
admin.site.register(state)
admin.site.register(religion)
admin.site.register(document)
admin.site.register(level)
admin.site.register(abroad)
admin.site.register(interest)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(page_source)
admin.site.register(loggedcount,loggedcountAdmin)
admin.site.register(Provider)
admin.site.register(question)
admin.site.register(answer)
admin.site.register(activity)
admin.site.register(Applicant)
admin.site.register(ShortList)
admin.site.register(Selected)
admin.site.register(Rejected)
admin.site.register(Note)

