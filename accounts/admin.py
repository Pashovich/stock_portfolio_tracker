# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User, Share, Portfolio

# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('name',)}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'name', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('email', 'name', 'is_staff', 'is_active')
#     list_filter = ('is_staff', 'is_active')
#     search_fields = ('email', 'name')
#     ordering = ('email',)

# admin.site.register(User, UserAdmin)
# admin.site.register(Share)
# admin.site.register(Portfolio)