from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'country')
    list_filter = ('birth', 'country')


admin.site.register(UserProfile, UserProfileAdmin)