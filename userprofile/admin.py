from django.contrib import admin
from django.contrib.admin import register

from userprofile.models import Profile


@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'get_firstname', 'get_lastname', 'jobTitle', 'company')

    def get_username(self, obj):
        return obj.user.username

    def get_firstname(self, obj):
        return obj.user.first_name

    def get_lastname(self, obj):
        return obj.user.last_name

    get_username.short_description = 'Username'
    get_firstname.short_description = 'First Name'
    get_lastname.short_description = 'Last Name'
