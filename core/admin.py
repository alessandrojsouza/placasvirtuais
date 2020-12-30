from django.contrib import admin

from core.models import User


class UserAdmin(admin.ModelAdmin):
  list_display = (
    'username',
    'get_full_name',
    'email',
    'date_joined',
    'is_active',
    'is_staff'
  )
  list_filter = ('is_active', 'is_staff', 'is_superuser')
  search_fields = (
    'first_name',
    'last_name',
    'username',
    'email',
    'expiration_date',
    'date_joined',
    'is_active',
    'is_staff'
  )
  ordering = ('-date_joined',)
  list_per_page = 14


admin.site.register(User, UserAdmin)
