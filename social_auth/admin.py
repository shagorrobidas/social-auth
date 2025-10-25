from django.contrib import admin
from .models import User, SocialAccount
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SocialAccount

# ------------------------------
# Custom User Admin
# ------------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to display in the admin list view
    list_display = ('email', 'name', 'is_staff', 'is_active', 'force_logout_required')
    list_filter = ('is_staff', 'is_active', 'gender')

    # Fields editable in the list view
    list_editable = ('is_active',)

    # Searchable fields
    search_fields = ('email', 'name', 'phone')

    # Ordering
    ordering = ('email',)

    # Fieldsets for detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'gender', 'description', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Info', {'fields': ('current_refresh_token', 'force_logout_required')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to use when creating a new user via admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )


# ------------------------------
# SocialAccount Admin
# ------------------------------
@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'uid')
    search_fields = ('user__email', 'provider', 'uid')
    list_filter = ('provider',)
