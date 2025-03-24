from django.contrib import admin
from .models import CustomUser, Profile


class CustomUserAdmin(admin.ModelAdmin):
    fields = ('id', 'username', 'email', 'password', 'is_superuser', 'is_staff')
    readonly_fields = ('id', )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)