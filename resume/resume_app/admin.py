from django.contrib import admin
from .models import CustomUser, Resume
from django.contrib.auth.admin import UserAdmin

# register admin
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Resume)