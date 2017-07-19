from django.contrib import admin
from .models import UserProfile

#class UserProfileAdmin(admin.ModelAdmin):
#	list_display = ('user', 'home_city', 'color_theme')

admin.site.register(UserProfile)