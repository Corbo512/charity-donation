from django.contrib import admin
from .models import Category, Institution, Donation, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
