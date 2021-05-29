from django.contrib import admin
from .models import User, Address
from django.contrib.auth.admin import UserAdmin
default_app_config = 'accounts.apps.AccountsConfig'
# Register your models here.
admin.site.register(Address)
admin.site.register(User)
