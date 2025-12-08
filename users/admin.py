from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'country', 'is_staff') # Что показывать в списке
    filter_horizontal = ('groups', 'user_permissions')       #  ВОТ ЭТА МАГИЯ