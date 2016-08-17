from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username', )
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        ('User', {'fields' : ('username', 'password')}),
        ('Personal info', {'fields' : ('first_name',
                                       'last_name',
                                       'email',
                                       'picture')}),
        ('Permissions', {'fields' : ('is_active',
                                     'is_staff',
                                     'is_superuser',
                                     'groups',
                                     'user_permissions')}),
    )    

admin.site.register(User, UserAdmin)
