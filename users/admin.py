from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User #, UserInfo


# class UserInfoStackedInline(admin.StackedInline):
#     model = UserInfo
#     max_num=1

class UserAdmin(BaseUserAdmin):
    # inlines = [UserInfoStackedInline, ]
    # ('image','full_name', 'phone_number', 'email', 'address', 'company', 'company_web_site', 'company_address',)
    fieldsets = (
        ('User Info', 
            {'fields': (
                'image',
                'full_name', 
                'phone_number', 
                'email', 
                'address', 
                'company', 
                'company_web_site', 
                'company_address',
                'phone_number_verified', 
                'change_pw',
            )
        }),
        ('User Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('full_name', 'phone_number', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'date_joined', 'phone_number_verified', 'change_pw',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('full_name', 'phone_number',)
    ordering = ('full_name', 'phone_number', )
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)